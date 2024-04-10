"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import pandas as pd
import json

def convertInputFilesToJSON(inp_folder:str = "input_files/", json_folder:str = "input_json/") -> None:

    """
    This utility function converts the input files (CSV format) to JSON

    Arguments
    ----------
    inp_folder: str
        the folder path to the CSV file you want to convert
    json_folder: str
        the folder path for the output files
        
    Returned Values
    ----------
    
    """

    input_file_names = ["TA_schedule.csv", "class_schedule.csv", "Instr_Pref.csv"]

    json_files = [pd.read_csv(inp_folder + filename).to_json() for filename in input_file_names]

    output_file_names = [filename.replace(".csv", ".json") for filename in input_file_names]

    for i in range(len(input_file_names)):
        with open(json_folder + output_file_names[i], 'w') as jsonfile:
            json.dump(json_files[i], jsonfile, indent=2)