import os
import subprocess

from symbols_db import DEBUG_MODE, VCPKG_HASH, VCPKG_LOCATION, VCPKG_URL, logger
from symbols_db.handlers.git_handler import git_checkout_commit, git_clone
from symbols_db.handlers.language_handlers import BaseHandler
from symbols_db.utils.utils import subprocess_run_debug


class VcpkgHandler(BaseHandler):

    def __init__(self):
        pass

    def build(self, project_name):
        pass

    def find_executables(self, project_name):
        pass

    def delete_project_files(self, project_name):
        pass

    def get_project_list(self):
        pass


def git_clone_vcpkg():
    git_clone(VCPKG_URL, VCPKG_LOCATION)


def git_checkout_vcpkg_commit():
    git_checkout_commit(VCPKG_LOCATION, VCPKG_HASH)


def run_vcpkg_install_command():
    # Linux command
    install_command = ["./bootstrap-vcpkg.sh"]
    install_run = subprocess.run(
        install_command, cwd=VCPKG_LOCATION, capture_output=True
    )
    if DEBUG_MODE:
        print(install_run.stdout)
        logger.debug(f'"bootstrap-vcpkg.sh: ":{install_run.stdout.decode('ascii')}')

    int_command = "./vcpkg integrate install".split(" ")
    int_run = subprocess.run(int_command, cwd=VCPKG_LOCATION, capture_output=True)
    if DEBUG_MODE:
        print(int_run.stdout)
        logger.debug(f'"vcpkg integrate install: ":{int_run.stdout.decode('ascii')}')


def get_vcpkg_projects():
    git_clone_vcpkg()
    git_checkout_vcpkg_commit()
    run_vcpkg_install_command()

    ports_path = VCPKG_LOCATION / "ports"
    return os.listdir(ports_path)

def vcpkg_build(project_name):
    inst_cmd = f"./vcpkg install {project_name}".split(" ")
    inst_run = subprocess.run(inst_cmd, cwd=VCPKG_LOCATION, capture_output=True)
    subprocess_run_debug(inst_run, project_name)

def exec_explorer(directory):
  """
  Walks through a directory and identifies executable files using the `file` command.

  Args:
    directory: The directory to search.

  Returns:
    A list of executable file paths.
  """
  executables = []
  for root, _, files in os.walk(directory):
    for file in files:
      file_path = os.path.join(root, file)
      try:
        result = subprocess.run(['file', file_path], capture_output=True)
        if b"ELF" in result.stdout:
            executables.append(file_path)
        if b"archive" in result.stdout:
            executables.append(file_path)
      except FileNotFoundError:
        print(
          f"Error: 'file' command not found. Make sure it's installed and in your PATH."
          )
        return []
  return executables

def archive_explorer(directory):
  """
  Walks through a directory and identifies executable files using the `file` command.

  Args:
    directory: The directory to search.

  Returns:
    A list of executable file paths.
  """
  executables = []
  for root, _, files in os.walk(directory):
    for file in files:
      file_path = os.path.join(root, file)
      try:
        result = subprocess.run(['file', file_path], capture_output=True)
        if b"archive" in result.stdout:
            executables.append(file_path)
      except FileNotFoundError:
        print(
          f"Error: 'file' command not found. Make sure it's installed and in your PATH."
          )
        return []
  return executables

def find_vcpkg_executables(project_name):
    # TODO: linux only
    project_path = project_name + "_x64-linux"
    target_directory = VCPKG_LOCATION / "packages" / project_path
    execs = exec_explorer(target_directory)

    return execs

