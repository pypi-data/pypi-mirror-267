"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

def getDaysMap() -> dict:

    """
    The function returns a dictionary which maps the weekday index string to the symbol

    Arguments
    ----------
        
    Returned Values
    ----------
    weekday_mapping : dict

    """ 

    return {
        "MONDAY_IND": "M",
        "TUESDAY_IND": "T",
        "WEDNESDAY_IND": "W",
        "THURSDAY_IND": "R",
        "FRIDAY_IND": "F"
    }