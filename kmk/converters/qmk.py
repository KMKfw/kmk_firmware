import json
import re

def read_qmk_config(path: str):
    json_data = {}
    with open(path, 'r') as config_file_handle:
        json_data = json.load(config_file_handle)
    key_map_data = [
        [parse_str_to_kmk_key(key) for key in layer] for layer in json_data['layers']
    ]
    return json_data['layers']


def parse_str_to_kmk_key(key: str):
    '''Pomsky Regex Code:
	let string = (['A'-'Z' '0'-'9' '_'])+;
	let number = ['0'-'9']+;

	# Match: LT(<Any Number>,<Any String>)
	| :layer('LT(' :layernum(number) ',' :layerkey(string) ')')

	# Match: LSFT_T(<Any String>)
	| :shiftmod('LSFT_T(' :shiftkey(string) ')')

	# Match: LCTL_T(<Any String>)
	| :ctrlmod('LCTL_T(' :ctrlkey(string) ')')

	# Match: LALT_T(<Any String>)
	| :altmod('LALT_T(' :altkey(string) ')')
    '''
    outer_regex = "(?P<layer>LT\((?P<layernum>[0-9]+),(?P<layerkey>[A-Z0-9_]+)\))|(?P<shiftmod>LSFT_T\((?P<shiftkey>[A-Z0-9_]+)\))|(?P<ctrlmod>LCTL_T\((?P<ctrlkey>[A-Z0-9_]+)\))|(?P<altmod>LALT_T\((?P<altkey>[A-Z0-9_]+)\))"
    
    '''
    'KC_' :keyname((['A'-'Z' '0'-'9' '_'])+)
    '''
    inner_regex = "KC_(?P<keyname>[A-Z0-9_]+)"
    
    outer_result = re.search(outer_regex, key)
    
    if outer_result:
        print(outer_result.groups())
    else:
        inner_result = re.search(inner_regex, key)
        print(inner_result)
        
    
    return key

def one_to_one_converter(key: str):
    return key

#print(read_qmk_config("full_size_normal_keys.json"))
print(read_qmk_config("special.json"))