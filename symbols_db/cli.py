import argparse
from symbols_db.handlers.cyclonedx_handler import get_purl_from_bom

from symbols_db.handlers.language_handlers.cargo_handler import build_crates_from_purl
from symbols_db.handlers.blint_handler import blint_on_crates_from_purl

def arguments_parser():
    parser = argparse.ArgumentParser(
        prog="symbols_db",
        description='Stores Symbols for rust binaries')
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
    
    return parser.parse_args()

def main():
    
    args = vars(arguments_parser())
    print(args['bom'])
    if args['add_cdxgen_db']:
        purllist = get_purl_from_bom(args['bom'])
        build_crates_from_purl(purllist)
        blint_on_crates_from_purl(purllist)
        # download_crate_from_purl(purllist)
    
    if args['add_blint_db']:
        

if __name__ == "__main__":
    main()