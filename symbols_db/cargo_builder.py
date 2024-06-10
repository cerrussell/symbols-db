import os
from utils import get_all_index_names, get_path_names_from_index_names, from_purl_to_rust_srcname

def build_crates_from_purl(purllist):
    indexes = get_all_index_names()
    package_locations = get_path_names_from_index_names(indexes)

    for package in purllist:
        purl = from_purl_to_rust_srcname(package)
        for package_location in package_locations:
            # print(os.path.join(package_location, purl))
            packages_available = os.listdir(package_location)
            if purl in packages_available:
                build_cargo_package(os.path.join(package_location, purl))
                break

def build_cargo_package(build_dir):
    print(build_dir)
    os.system(f"cargo build --manifest-path={build_dir}/Cargo.toml")