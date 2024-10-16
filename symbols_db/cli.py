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
        "--cdxgen-report",
        dest="report",
        help="Path to the CDXGEN report file",
    )
    
    return parser.parse_args()

def main():
    print("this was just added")
    args = arguments_parser()
    print(args.report)
    purllist = get_purl_from_bom(args.report)
    build_crates_from_purl(purllist)
    blint_on_crates_from_purl(purllist)
    # download_crate_from_purl(purllist)

if __name__ == "__main__":
    main()