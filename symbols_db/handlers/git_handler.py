import os
import subprocess
from pathlib import Path

from symbols_db import WRAPDB_LOCATION
from symbols_db import logger

# TODO: debug mode
DEBUG_MODE = True


# TODO: error checking here
def git_clone_wrapdb():
    # TODO: handle and print output of command
    command = (
        f"git clone https://github.com/mesonbuild/wrapdb.git {WRAPDB_LOCATION}".split(
            " "
        )
    )
    subprocess_output = subprocess.run(command, capture_output=True)
    if DEBUG_MODE:
        print(subprocess_output.stdout)


def git_checkout_wrapdb_commit():
    # TODO: change commit hash, it is the lastest one at the time of writing
    command = f"git -C {WRAPDB_LOCATION} checkout 90fdc28c75412d99900f2ff58006de57866c63ee".split(
        " "
    )
    subprocess_output = subprocess.run(command, capture_output=True)
    if DEBUG_MODE:
        print(subprocess_output.stdout)


def get_wrapdb_projects():
    git_clone_wrapdb()
    git_checkout_wrapdb_commit()
    subproject_filenames = os.listdir(WRAPDB_LOCATION / "subprojects")
    projects_list = []
    for file in subproject_filenames:
        project_path = Path(file)
        if project_path.suffix == ".wrap":
            projects_list.append(project_path.stem)
    return projects_list
