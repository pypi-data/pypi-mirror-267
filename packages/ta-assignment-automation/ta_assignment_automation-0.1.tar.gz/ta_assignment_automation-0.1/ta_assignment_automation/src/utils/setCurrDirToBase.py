"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import os
import sys

def setCurrDirToBase() -> None:
    """
    This function sets the Current Directory to the Base (Project folder)

    Arguments
    ----------
        
    Returned Values
    ----------

    """

    # Get the current working directory
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Add the parent directory to sys.path
    parent_path = os.path.join(current_path, '..')
    sys.path.append(parent_path)
