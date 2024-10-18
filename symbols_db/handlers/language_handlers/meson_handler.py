import os
import subprocess

from symbols_db import logger, WRAPDB_LOCATION, CWD
from pathlib import Path
from symbols_db import logger


# TODO: debug
DEBUG_MODE = True


def meson_build(project_name):
    setup_command = f"meson setup build/{project_name} -Dwraps={project_name}".split(
        " "
    )
    meson_setup = subprocess.run(setup_command, cwd=WRAPDB_LOCATION)
    if DEBUG_MODE:
        print(meson_setup.stdout)
        print(meson_setup.stderr)
        if meson_setup.stderr:
            logger.error(
                f"{project_name} failed to SETUP {WRAPDB_LOCATION/'build'/project_name}"
            )
    compile_command = f"meson compile -C build/{project_name}".split(" ")
    meson_compile = subprocess.run(compile_command, cwd=WRAPDB_LOCATION)
    if DEBUG_MODE:
        print(meson_compile.stdout)
        print(meson_compile.stderr)
        if meson_compile.stderr:
            logger.error(
                f"{project_name} failed to COMPILE {WRAPDB_LOCATION/'build'/project_name}"
            )


def find_executables(project_name):
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


def strip_executables(file_path):
    strip_command = f"strip --strip-all {file_path}".split(" ")
    subprocess.run(strip_command, cwd=WRAPDB_LOCATION)
