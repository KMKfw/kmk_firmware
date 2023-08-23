import json


def read_qmk_config(path: str):
    json_data = {}
    with open(path, "r") as config_file_handle:
        json_data = json.load(config_file_handle)
    key_map_data = [
        [parse_str_to_kmk_key(key) for key in layer] for layer in json_data["layers"]
    ]
    return json_data["layers"]


def parse_str_to_kmk_key(key: str):
    # TODO: Parse key strings
    return key
