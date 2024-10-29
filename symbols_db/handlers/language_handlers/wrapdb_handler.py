import os
from pathlib import Path
from symbols_db import WRAPDB_HASH, WRAPDB_LOCATION, WRAPDB_URL
from symbols_db.handlers.git_handler import git_checkout_commit, git_clone


def git_clone_wrapdb():
    git_clone(WRAPDB_URL, WRAPDB_LOCATION)


def git_checkout_wrapdb_commit():
    git_checkout_commit(WRAPDB_LOCATION, WRAPDB_HASH)


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
