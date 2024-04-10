"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import csv

def read_csv_to_dict(file_path: str) -> list:

    """
    This utility function reads a CSV file (the path is given as the input parameter) and returns a list of dictionaries.

    Arguments
    ----------
    file_path: str
        the file path to the CSV file you want to convert
        
    Returned Values
    ----------
    data_dict_list: list
        list of dictionaries converted from the CSV file

    """

    data_dict_list = []

    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data_dict_list.append(row)

    return data_dict_list