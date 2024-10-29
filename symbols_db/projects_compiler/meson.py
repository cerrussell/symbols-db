import shutil

from symbols_db import WRAPDB_HASH, WRAPDB_LOCATION, WRAPDB_URL
from symbols_db.handlers.git_handler import git_checkout_commit, git_clone


def git_clone_wrapdb():
    git_clone(WRAPDB_URL, WRAPDB_LOCATION)


def git_checkout_wrapdb_commit():
    git_checkout_commit(WRAPDB_LOCATION, WRAPDB_HASH)


def ensure_meson_installed():
    return shutil.which("meson") is not None
