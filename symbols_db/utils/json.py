import json
from symbols_db import logger

def get_key_in_json_list(key_search, key_name, property_list):
    return_key = None
    for i in property_list:
        if i[key_name] == key_search:
            return_key = i
    if return_key:
        return return_key
    else:
        raise Exception("Spelling mistake probably")


def get_properties_internal(property_name, file_name):
    blint_sbom = None
    with open(file_name, "r") as f:
        blint_sbom = json.load(f)

    properties = blint_sbom["metadata"]["component"]["properties"]
    req_property = get_key_in_json_list(property_name, "name", properties)

    return req_property["value"]
