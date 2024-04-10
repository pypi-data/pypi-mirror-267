"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

def saveMatToTxt(matrix: dict, output_path: str="output_files/conflict_matrix.txt") -> None:

    """
    This function takes the conflict matix as input and stores it in a text file.

    Arguments
    ----------
    matrix: dict
        the conflict matrix
    output_path: str
        the path to the text file where you want to store the matrix
        
    Returned Values
    ----------
    None

    """

    # Get the number of rows
    num_rows = len(matrix)

    # Find the maximum column number in the matrix
    max_columns = max(max(inner.keys(), default=0) for inner in matrix.values())

    # Create a 2D list to store the values
    conf_matrix = [
        [matrix[i].get(j, 0) for j in range(1, max_columns + 1)] for i in range(1, num_rows + 1)
    ]
    
    # conf_matrix = [
    #     [matrix[ta_id].get(j, 0) for j in range(1, max_columns + 1)] for ta_id in matrix
    # ]

    # Write the data to a text file
    with open(output_path, 'w') as file:
        for row in conf_matrix:
            file.write(' '.join(map(str, row)) + '\n')
    print("CONFLICT MATRIX SAVED TO ", output_path)