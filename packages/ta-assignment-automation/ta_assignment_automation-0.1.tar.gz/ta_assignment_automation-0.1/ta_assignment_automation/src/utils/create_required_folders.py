"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 04/10/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""
import os

def create_required_folders()->None:
    """
    This utility function creates all the required folders for this project to work.
    The required folder path is present in the folder_list list (will create recursively if path is provided)

    Arguments
    ----------
    None
        
    Returned Values
    ----------
    None

    """

    folder_list = ["input_files", "input_json", "output_files/section_data", "assignment_output_files"]

    for folder_path in folder_list:
        os.makedirs(folder_path, exist_ok=True)