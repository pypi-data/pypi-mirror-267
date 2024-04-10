"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

def getConflictMatFromTxt(input_path:str ="output_files/conflict_matrix.txt") -> list:

    """
    This utility function returns the conlict matrix in a list of mappings format from the text file

    Arguments
    ----------
    input_path: str
        the path to the conflict matrix text file
        
    Returned Values
    ----------
    conf_matrix: list
        the conflict matrix

    """

    # Read the data from the text file
    with open(input_path, 'r') as file:
        lines = file.readlines()

    # Create a list of lists
    conf_matrix = [list(map(int, line.strip().split())) for line in lines]
    
    print("Conflict matix loaded to use in algo")

    return conf_matrix