"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json

def write_dict_to_json(data_list:list , json_file_path:str) -> None:
    
    """
    This utility function takes the data list and stores it in a json file

    Arguments
    ----------
    file_path: str
        the list data that you want to store in json file
    json_file_path: str
        the path to json file that you want to store the data in
        
    Returned Values
    ----------
    None

    """

    with open(json_file_path, 'w') as jsonfile:
        json.dump(data_list, jsonfile, indent=2)