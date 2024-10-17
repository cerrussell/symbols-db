import argparse
import concurrent
import concurrent.futures
from time import sleep

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


def arguments_parser():
    parser = argparse.ArgumentParser(
        prog="symbols_db", description="Stores Symbols for rust binaries"
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


def build_run_blint_projects(project_list):
    # returns executables list so we can run blint on them
    executables_list = []
    for project_name in project_list:
        pid = add_projects(project_name)
        meson_build(project_name)
        execs = find_executables(project_name)
        for files in execs:

            strip_executables(files, pid)
            bid = add_binary(
                files,
            )
            if_list = get_blint_internal_functions_exe(files)
            for func in if_list:
                add_binary_export(func, bid)

        executables_list.extend(execs)
    return executables_list


def meson_add_blint_bom_process(blintsbom):
    # get the list of project to be build
    projects_list = get_wrapdb_projects()

    # build the projects parallely
    build_run_blint_projects(projects_list)

    # create blint for each project

    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        parallel_futures = [executor.submit(sleep, 5)]
        concurrent.futures.wait(parallel_futures)


def main():

    args = vars(arguments_parser())
    print(args["bom"])
    if args["add_cdxgen_db"]:
        purllist = get_purl_from_bom(args["bom"])
        build_crates_from_purl(purllist)
        blint_on_crates_from_purl(purllist)
        # download_crate_from_purl(purllist)

    if args["auto"]:
        meson_add_blint_bom_process(args["blintsbom"])

    if args["add_blint_db"]:
        pass


if __name__ == "__main__":
    main()
