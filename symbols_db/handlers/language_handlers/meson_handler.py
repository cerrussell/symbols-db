import os
import subprocess
from pathlib import Path

from symbols_db import CWD, WRAPDB_LOCATION
from symbols_db.handlers.language_handlers import BaseHandler
from symbols_db.projects_compiler.meson import (ensure_meson_installed,
                                                git_checkout_wrapdb_commit,
                                                git_clone_wrapdb)
from symbols_db.utils.utils import subprocess_run_debug


class MesonHandler(BaseHandler):

    def __init__(self):
        if ensure_meson_installed():
            git_clone_wrapdb()
            git_checkout_wrapdb_commit()
        else:
            ModuleNotFoundError("Meson was not found")

    def build(self, project_name):
        setup_command = (
            f"meson setup build/{project_name} -Dwraps={project_name}".split(" ")
        )
        meson_setup = subprocess.run(setup_command, cwd=WRAPDB_LOCATION)
        subprocess_run_debug(meson_setup, project_name)
        compile_command = f"meson compile -C build/{project_name}".split(" ")
        meson_compile = subprocess.run(compile_command, cwd=WRAPDB_LOCATION)
        subprocess_run_debug(meson_compile, project_name)

    def find_executables(self, project_name):
        full_project_dir = WRAPDB_LOCATION / "build" / project_name / "subprojects"
        executable_list = []
        for root, dir, files in os.walk(full_project_dir):
            for file in files:
                # what is the value of variable `root`
                file_path = Path(root) / file
                if os.access(file_path, os.X_OK):
                    full_path = CWD / file_path
                    file_output = subprocess.run(
                        ["file", full_path], capture_output=True
                    )
                    if b"ELF" in file_output.stdout:
                        executable_list.append(full_path)
        return executable_list

    def delete_project_files(self, project_name):
        pass

    def get_project_list(self):
        subproject_filenames = os.listdir(WRAPDB_LOCATION / "subprojects")
        projects_list = []
        for file in subproject_filenames:
            project_path = Path(file)
            if project_path.suffix == ".wrap":
                projects_list.append(project_path.stem)
        return projects_list


def meson_build(project_name):
    setup_command = f"meson setup build/{project_name} -Dwraps={project_name}".split(
        " "
    )
    meson_setup = subprocess.run(setup_command, cwd=WRAPDB_LOCATION)
    subprocess_run_debug(meson_setup, project_name)
    compile_command = f"meson compile -C build/{project_name}".split(" ")
    meson_compile = subprocess.run(compile_command, cwd=WRAPDB_LOCATION)
    subprocess_run_debug(meson_compile, project_name)


def find_meson_executables(project_name):
    full_project_dir = WRAPDB_LOCATION / "build" / project_name / "subprojects"
    executable_list = []
    for root, dir, files in os.walk(full_project_dir):
        for file in files:
            # what is the value of variable `root`
            file_path = Path(root) / file
            if os.access(file_path, os.X_OK):
                full_path = CWD / file_path
                file_output = subprocess.run(["file", full_path], capture_output=True)
                if b"ELF" in file_output.stdout:
                    executable_list.append(full_path)
    return executable_list


def strip_executables(file_path, loc=WRAPDB_LOCATION):
    strip_command = f"strip --strip-all {file_path}".split(" ")
    subprocess.run(strip_command, cwd=loc)
