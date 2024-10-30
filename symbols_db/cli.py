import argparse
import concurrent

from symbols_db.handlers.language_handlers.vcpkg_handler import \
    get_vcpkg_projects
from symbols_db.handlers.language_handlers.wrapdb_handler import \
    get_wrapdb_projects
from symbols_db.handlers.sqlite_handler import (clear_sqlite_database,
                                                create_database)
from symbols_db.projects_compiler.meson import mt_meson_blint_db_build
from symbols_db.projects_compiler.vcpkg import mt_vcpkg_blint_db_build


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
    parser.add_argument(
        "--clean-start",
        dest="clean",
        default=False,
        action="store_true",
        help="Resets the database before starting a new build"
    )

    return parser.parse_args()


def meson_add_blint_bom_process(blintsbom):  #TODO: remove argument if not used
    projects_list = get_wrapdb_projects()

    # build the projects single threaded
    # st_meson_blint_db_build(projects_list)

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for project_name, executables in zip(
            projects_list, executor.map(mt_meson_blint_db_build, projects_list)
        ):
            print(f"Ran complete for {project_name} and we found {len(executables)}")


def vcpkg_add_blint_bom_process(blintsbom):  #TODO: remove argument if not used
    projects_list = get_vcpkg_projects()

    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        for project_name, executables in zip(
            projects_list, executor.map(mt_vcpkg_blint_db_build, projects_list)
        ):
            print(f"Ran complete for {project_name} and we found {len(executables)}")


def main():

    args = vars(arguments_parser())

    if args["clean"]:
        clear_sqlite_database()
        create_database()

    if args["meson"]:
        meson_add_blint_bom_process(args["blintsbom"])

    if args["vcpkg"]:
        vcpkg_add_blint_bom_process(args["blintsbom"])


if __name__ == "__main__":
    main()
