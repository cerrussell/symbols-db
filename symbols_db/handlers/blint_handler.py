import json
import os
from pathlib import Path
import subprocess

from symbols_db import BOM_LOCATION, CWD
from symbols_db.handlers.sqlite_handler import store_sbom_in_sqlite
from symbols_db.utils.json import get_properties_internal
from symbols_db.utils.rust import (
    from_purl_to_rust_srcname,
    get_all_index_names,
    get_path_names_from_index_names,
)
from symbols_db import DEBUG_MODE, DELIMETER_BOM, WRAPDB_LOCATION
from symbols_db import logger


class BlintBom:

    def __init__(
        self,
        bomFormat=None,
        specVersion=None,
        serialNumber=None,
        metadata=None,
        components=None,
        dependencies=None,
        bom_string=None,
    ):
        # self.bomFormat = bomFormat
        # self.specVersion = specVersion
        # self.serialNumber = serialNumber
        # self.metadata = metadata
        # self.components = components
        # self.dependencies = dependencies
        # TODO: remove bom_string and properly hanlde serialization and de
        self.bom_string = None


class Components:
    def __init__(
        self,
        comp_type=None,
        bom_ref=None,
        name=None,
        scope=None,
        purl=None,
        evidence=None,
        properties=None,
    ):
        self.comp_type = comp_type
        self.bom_ref = bom_ref
        self.name = name
        self.scope = scope
        self.purl = purl
        self.evidence = evidence
        self.properties = properties


def run_blint_on_file(file_path):
    # TODO: assume blint installed
    blint_command = f"blint sbom --deep -o {file_path}.json -i {file_path}".split(" ")
    blint_output = subprocess.run(blint_command, cwd=WRAPDB_LOCATION)

    if DEBUG_MODE:
        print(blint_output.stdout)
        print(blint_output.stderr)


def get_blint_file(project_name):
    # run after blint was running
    blint_file = BOM_LOCATION / project_name / ".json"
    blint_str = None
    with open(blint_file, "r") as f:
        blint_str = f.read()
    return blint_str


def get_blint_internal_functions_exe(file_path):
    # here the file path is relative, we make it complete

    run_blint_on_file(file_path)
    blint_file = Path(str(file_path) + ".json")

    if_string = get_properties_internal("internal:functions", blint_file)
    return if_string.split(DELIMETER_BOM)


def run_blint(build_dir, package_name):
    os.system(
        f"blint sbom -i {build_dir} -o {build_dir}/sbom.json --exports-prefix {package_name}"
    )


def get_sbom_json(build_dir):
    with open(os.path.join(build_dir, "sbom.json")) as sbom_file:
        data = sbom_file.read()
        return data


def blint_on_crates_from_purl(purllist):
    indexes = get_all_index_names()
    package_locations = get_path_names_from_index_names(indexes)

    for package in purllist:
        package_name = package.split("@")[0].split("/")[1]
        purl = from_purl_to_rust_srcname(package)
        for package_location in package_locations:
            # print(os.path.join(package_location, purl))
            packages_available = os.listdir(package_location)
            if purl in packages_available:
                run_blint(os.path.join(package_location, purl), package_name)
                data = get_sbom_json(os.path.join(package_location, purl))
                store_sbom_in_sqlite(package, data)
                break
