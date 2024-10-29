import argparse
import concurrent
import concurrent.futures
import sqlite3
import traceback
from time import sleep

from symbols_db import BLINTDB_LOCATION, VCPKG_LOCATION, logger
from symbols_db.handlers.blint_handler import (
    blint_on_crates_from_purl,
    get_blint_internal_functions_exe,
)
from symbols_db.handlers.cyclonedx_handler import get_purl_from_bom
from symbols_db.handlers.language_handlers.cargo_handler import build_crates_from_purl
from symbols_db.handlers.language_handlers.meson_handler import (
    find_meson_executables,
    meson_build,
    strip_executables,
)
from symbols_db.handlers.language_handlers.vcpkg_handler import (
    find_vcpkg_executables,
    get_vcpkg_projects,
    vcpkg_build,
)
from symbols_db.handlers.language_handlers.wrapdb_handler import get_wrapdb_projects

# TODO: clean up reset database command
from symbols_db.handlers.sqlite_handler import (
    add_binary,
    add_binary_export,
    add_projects,
    clear_sqlite_database,
    create_database,
)

clear_sqlite_database()
create_database()


def arguments_parser():
    parser = argparse.ArgumentParser(
        prog="symbols_db", description="Stores Symbols for binaries"
    )
    parser.add_argument(
        "-c",
        "--cdxgen-bom",
        dest="cdxgen_bom",
        help="Path to the CDXGEN bom file (NOT IMPLEMENTED)",
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
        help="Path to the Blint SBOM for a binary (NOT IMPLEMENTED)",
    )
    parser.add_argument(
        "-bs",
        "--add-blint-db",
        dest="add_blint_db",
        action="store_true",
        help="This flag allows to add blint SBOM to Database",
    )
    parser.add_argument(
        "-Z1",
        "--meson-blintdb",
        dest="meson",
        action="store_true",
        help="This flag starts the automatic blintdb build using wrapdb packages",
    )
    parser.add_argument(
        "-Z2",
        "--vcpkg-blintdb",
        dest="vcpkg",
        action="store_true",
        help="This flag starts the automatic blintdb build using vcpkg packages",
    )

    return parser.parse_args()


def add_project_meson_db(project_name):
    pid = add_projects(project_name)
    meson_build(project_name)
    execs = find_meson_executables(project_name)
    for files in execs:
        strip_executables(files)
        bid = add_binary(files, pid)
        if_list = get_blint_internal_functions_exe(files)
        for func in if_list:
            add_binary_export(func, bid)

    # delete project after done processing

    return execs


def st_meson_blint_db_build(project_list):
    # returns executables list so we can run blint on them
    executables_list = []
    for project_name in project_list:
        execs = add_project_meson_db(project_name)

        executables_list.extend(execs)
    return executables_list


def mt_meson_blint_db_build(project_name):
    logger.debug(f"Running {project_name}")
    try:
        execs = add_project_meson_db(project_name)
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
    # st_meson_blint_db_build(projects_list)

    # build projects multiprocess
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for project_name, executables in zip(
            projects_list, executor.map(mt_meson_blint_db_build, projects_list)
        ):
            print(f"Ran complete for {project_name} and we found {len(executables)}")


def add_project_vcpkg_db(project_name):
    pid = add_projects(project_name)
    vcpkg_build(project_name)
    execs = find_vcpkg_executables(project_name)
    for files in execs:
        # strip_executables(files, VCPKG_LOCATION)
        bid = add_binary(files, pid, split_word="packages/")
        if_list = get_blint_internal_functions_exe(files)
        for func in if_list:
            add_binary_export(func, bid)

    # delete project after done processing

    return execs


def mt_vcpkg_blint_db_build(project_name):
    logger.debug(f"Running {project_name}")
    try:
        execs = add_project_vcpkg_db(project_name)
    except Exception as e:
        logger.info(f"error encountered with {project_name}")
        logger.error(e)
        logger.error(traceback.format_exc())
        return [False]
    return execs


def vcpkg_add_blint_bom_process(blintsbom):
    # get the list of project to be build
    projects_list = get_vcpkg_projects()

    # build projects multiprocess
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        for project_name, executables in zip(
            projects_list, executor.map(mt_vcpkg_blint_db_build, projects_list)
        ):
            print(f"Ran complete for {project_name} and we found {len(executables)}")


def main():

    args = vars(arguments_parser())

    if args["meson"]:
        meson_add_blint_bom_process(args["blintsbom"])

    if args["vcpkg"]:
        vcpkg_add_blint_bom_process(args["blintsbom"])


if __name__ == "__main__":
    main()
