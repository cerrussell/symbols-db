import os

def download_crate_from_purl(purllist):
    for purl in purllist:
        os.system(f'cargo install {purl}')