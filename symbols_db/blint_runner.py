import os
from utils import get_all_index_names, get_path_names_from_index_names, from_purl_to_rust_srcname
import json
from sqlite_handler import store_sbom_in_sqlite

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

def run_blint(build_dir, package_name):
    os.system(f"blint sbom -i {build_dir} -o {build_dir}/sbom.json --exports-prefix {package_name}")

def get_sbom_json(build_dir):
    with open(os.path.join(build_dir, "sbom.json")) as sbom_file:
        data = sbom_file.read()
        return data