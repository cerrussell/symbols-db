import json
from symbols_db import logger

def get_purl_from_bom(datafile):
    with open(f"{datafile}") as bom_file:
        data = json.load(bom_file)
        packages = data["components"]
        purllist = list()
        for i in packages:
            purl = i["purl"]
            purllist.append(purl[4:])
    return purllist
