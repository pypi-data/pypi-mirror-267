"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

def getLabTAReq() -> dict:

    """
    The function returns a dictionary which maps labs to the number of sections 1 TA can handle

    Arguments
    ----------
    
    Returned Values
    ----------
    lab_ta_requirement : dict

    ------------------------------------------------------------------------------------------

    Current Implementation based on these values: 
    "CSCI1300L": 2, (Total 2)
    "CSCI1301L": 3, (Total 22)
    "CSCI1302": 1,  (Total 6)
    "CSCI1730": 4,  (Total 8)
    "CSCI2150L": 4, (Total 4)
    "CSCI3030": 4,  (Total 8)


    1302 - No CRN splitting. One TA will handle one CRN

    1730, 3030 -> Half split. 2 TAs

    2150, 1300 -> Full Merge. One TA will handle all CRNs

    1301L -> Special Case. 22 CRNs, 7 TAs. One TA handles 3 CRNs

    ------------------------------------------------------------------------------------------

    """ 
    
    return {
        "CSCI1300L": 2,
        "CSCI1301L": 3,     # One TA can handle 3 sections  - 22 labs = 7 TAs (assign the last one to one of the TA)
        "CSCI1302": 1,      # Asked the current TA how they are assigned (5 TAs for 6 crns)
        "CSCI1730": 4,
        "CSCI2150L": 4,     # The labs are 1hr 15/20 mins which will be 5 hours per week. (Downside: 3 labs in one day)
        "CSCI3030": 4,
    }