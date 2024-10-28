import subprocess


# TODO: debug mode
DEBUG_MODE = True


# def git_clone_wrapdb():
#     command = (
#         f"git clone https://github.com/mesonbuild/wrapdb.git {WRAPDB_LOCATION}".split(
#             " "
#         )
#     )
#     subprocess_output = subprocess.run(command, capture_output=True)
#     if DEBUG_MODE:
#         print(subprocess_output.stdout)


def git_clone(git_url, loc):
    # TODO: error checking here
    # TODO: handle and print output of command
    command = f"git clone {git_url} {loc}".split(" ")
    proc_output = subprocess.run(command, capture_output=True)
    if DEBUG_MODE:
        print(proc_output.stdout)


# def git_checkout_wrapdb_commit():
#     # TODO: change commit hash, it is the lastest one at the time of writing
#     command = f"git -C {WRAPDB_LOCATION} checkout 90fdc28c75412d99900f2ff58006de57866c63ee".split(
#         " "
#     )
#     subprocess_output = subprocess.run(command, capture_output=True)
#     if DEBUG_MODE:
#         print(subprocess_output.stdout)


def git_checkout_commit(loc, commit_hash):
    command = f"git -C {loc} {commit_hash}".split(" ")
    proc_output = subprocess.run(command, capture_output=True)
    if DEBUG_MODE:
        print(proc_output.stdout)
