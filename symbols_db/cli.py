import argparse
from bom import get_purl_from_bom

from cargo_builder import build_crates_from_purl
from blint_runner import blint_on_crates_from_purl

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
    args = arguments_parser()
    print(args.report)
    purllist = get_purl_from_bom(args.report)
    build_crates_from_purl(purllist)
    blint_on_crates_from_purl(purllist)
    # download_crate_from_purl(purllist)

if __name__ == "__main__":
    main()