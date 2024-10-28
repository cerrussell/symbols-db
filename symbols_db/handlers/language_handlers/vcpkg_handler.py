import os
import subprocess

from symbols_db import DEBUG_MODE, VCPKG_HASH, VCPKG_LOCATION, VCPKG_URL
from symbols_db.handlers.git_handler import git_checkout_commit, git_clone
from symbols_db.handlers.language_handlers import BaseHandler


class VcpkgHandler(BaseHandler):

    def __init__():
        pass

    def build(project_name):
        pass

    def find_executables(project_name):
        pass

    def delete_project_files(project_name):
        pass

    def get_project_list():
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

    int_command = f"./vcpkg integrate install".split(" ")
    int_run = subprocess.run(int_command, cwd=VCPKG_LOCATION, capture_output=True)
    if DEBUG_MODE:
        print(int_run.stdout)


def get_vcpkg_projects():
    git_clone_vcpkg()
    git_checkout_vcpkg_commit()
    run_vcpkg_install_command()

    ports_path = VCPKG_LOCATION / "ports"
    ports = os.listdir(ports_path)
    return ports

def vcpkg_build(project_name):
    inst_cmd = f"./vcpkg install {project_name}".split(" ")
    inst_setup = subprocess.run(inst_cmd, cwd=VCPKG_LOCATION, capture_output=True)
    if DEBUG_MODE:
        print(inst_setup.stdout)

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
        if b"archive" in result.stdout:
            executables.append(file_path)
            print(file_path)
        if b"ELF" in result.stdout:
            executables.append(file_path)
            print(file_path)
      except FileNotFoundError:
        print(
          f"Error: 'file' command not found. Make sure it's installed and in your PATH."
          )
        return []
  return executables

def find_vcpkg_executables(project_name):
    target_directory = VCPKG_LOCATION
    execs = exec_explorer(target_directory)
    return execs

