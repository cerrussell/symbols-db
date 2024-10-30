import json


def get_purl_from_bom(datafile):
    with open(f"{datafile}") as bom_file:  # TODO: Add encoding, mode
        data = json.load(bom_file)
        packages = data["components"] # TODO: Do we need to do this with the file open?
        purllist = []
        for i in packages:
            purl = i["purl"]
            purllist.append(purl[4:])
    return purllist
