"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

def getEdgeWeights() -> dict:
    
    """

    This function returns a mapping of the weights assigned to each type of issues which are mentioned in the inline comments

    Arguments
    ----------
        
    Returned Values
    ----------
    weight_mapping: dict

    """
    
    return {
        "time_conflict": 1000,          # if TA schedule conflicts with the current section - LAB
        "current_course": 900,          # If they are currently enrolled in this section (make sure to do that for course)
        "not_ta_for_class_before": 5,   # did not TA for this class before
        "not_ins_pref": 4,              # is not in the preference list given by the instructor
        "not_taken_before": 3,          # did not take this course before
        "not_avail_at_class_time": 2,   # is not available during class time
        "not_first_pref": 1             # not the first preference of the instructor
    }
