"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""


# NUMBER OF STUDENTS : NO OF TAs
def getCapacityCap() -> list:

    """
    The function returns a list which maps the number of TAs required for the class to the total number of students in the class

    Arguments
    ----------
        
    Returned Values
    ----------
    class_capacity_to_TA : list
    """ 
    
    return {
        0.5: 22,           # 0.5 -> Number of TAs in the class, 22 -> Minimum number of students in the class 
        1: 45,            
        2: 90
    }