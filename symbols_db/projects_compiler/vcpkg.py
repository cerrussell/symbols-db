import subprocess

from symbols_db import (DEBUG_MODE, VCPKG_HASH, VCPKG_LOCATION, VCPKG_URL,
                        logger)
from symbols_db.handlers.git_handler import git_checkout_commit, git_clone


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
                result = subprocess.run(["file", file_path], capture_output=True)
                if b"ELF" in result.stdout:
                    executables.append(file_path)
                if b"archive" in result.stdout:
                    executables.append(file_path)
            except FileNotFoundError:
                print(
                    "Error: 'file' command not found. Make sure it's installed and in your PATH."
                )
                return []
    return executables
