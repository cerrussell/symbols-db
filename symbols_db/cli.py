import argparse
import concurrent
import concurrent.futures
from time import sleep
import sqlite3
import traceback

from symbols_db.handlers.blint_handler import (
    blint_on_crates_from_purl,
    get_blint_internal_functions_exe,
)
from symbols_db.handlers.cyclonedx_handler import get_purl_from_bom
from symbols_db.handlers.git_handler import get_wrapdb_projects
from symbols_db.handlers.language_handlers.cargo_handler import build_crates_from_purl
from symbols_db.handlers.language_handlers.meson_handler import (
    meson_build,
    find_executables,
    strip_executables,
)
from symbols_db.handlers.sqlite_handler import (
    add_projects,
    add_binary,
    add_binary_export,
)

# TODO:remove
from symbols_db.handlers.sqlite_handler import clear_sqlite_database, create_database
from symbols_db import BLINTDB_LOCATION, logger

# clear_sqlite_database()
create_database()

# Logging



def arguments_parser():
    parser = argparse.ArgumentParser(
        prog="symbols_db", description="Stores Symbols for binaries"
    )
    parser.add_argument(
        "-c",
        "--cdxgen-bom",
        dest="bom",
        help="Path to the CDXGEN bom file",
    )
    parser.add_argument(
        "-cs",
        "--add-cdxgen-db",
        dest="add_cdxgen_db",
        action="store_true",
        help="This flag allows to add Cdxgen BOM to Database",
    )
    parser.add_argument(
        "-b",
        "--blint-sbom",
        dest="blintsbom",
        help="Path to the Blint SBOM for a binary",
    )
    parser.add_argument(
        "-bs",
        "--add-blint-db",
        dest="add_blint_db",
        action="store_true",
        help="This flag allows to add blint SBOM to Database",
    )
    parser.add_argument("-Z", "--autogenerate-db", dest="auto", action="store_true")

    return parser.parse_args()


def build_and_database(project_name):
    pid = add_projects( project_name)
    meson_build(project_name)
    execs = find_executables(project_name)
    for files in execs:
        strip_executables(files)
        bid = add_binary(files, pid)
        if_list = get_blint_internal_functions_exe(files)
        for func in if_list:
            add_binary_export(func, bid)
    
    # delete project after done processing

    return execs

def bduild_run_blint_projects(project_list):
    # returns executables list so we can run blint on them
    executables_list = []
    for project_name in project_list:
        execs = build_and_database(project_name)

        executables_list.extend(execs)
    return executables_list

def build_run_blint(project_name):
    #
    logger.debug(f'Running {project_name}')
    try:
        execs = build_and_database(project_name)
    except Exception as e:
        logger.info(f"error encountered with {project_name}")
        logger.error(e)
        logger.error(traceback.format_exc())
        return [False]
    return execs

def meson_add_blint_bom_process(blintsbom):
    # get the list of project to be build
    projects_list = get_wrapdb_projects()

    # build the projects single threaded
    # build_run_blint_projects(projects_list)

    # build projects multiprocess
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for project_name, executables in zip(projects_list, executor.map(build_run_blint, projects_list)):
            print(f"Ran complete for {project_name} and we found {len(executables)}")


def main():

    args = vars(arguments_parser())
    
    if args["add_cdxgen_db"]:
        # Has been replaced
        pass
        # purllist = get_purl_from_bom(args["bom"])
        # build_crates_from_purl(purllist)
        # blint_on_crates_from_purl(purllist)
        # # download_crate_from_purl(purllist)

    if args["auto"]:
        meson_add_blint_bom_process(args["blintsbom"])

    if args["add_blint_db"]:
        pass


if __name__ == "__main__":
    main()
