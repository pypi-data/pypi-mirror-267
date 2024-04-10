"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json
from copy import deepcopy



from ..utils.dictionaryToJsonFile import write_dict_to_json

def incremental_TA_duplication() -> None:

    """
    This function picks the TA (non-duplicate) with the least enrollment for the class they are assigned to and duplicates them

    Arguments
    ----------
        
    Returned Values
    ----------
    None

    """

    with open("output_files/ta_schedule.json", 'r') as file:
        ta_schedule = json.load(file)

    with open("assignment_output_files/ta_assignments.json", 'r') as file:
        assignments = json.load(file)

    end_index = max(ta["ta_id"] for ta in ta_schedule) # get the last id

    already_double_TAs = []
    ta_check = set()

    for ta in ta_schedule:
        ta_name = ta["fname"] + ta["lname"] 
        if ta_name in ta_check:
            already_double_TAs.append(ta_name)
        else:
            ta_check.add(ta_name)

    assignments = sorted(assignments, key=lambda d: d['enrolled'])

    extraTAId = None

    for assignment in assignments:
        if extraTAId != None:
            break
        extra_name = assignment["fname"] + assignment["lname"] 
        if extra_name not in already_double_TAs:
            extraTAId = assignment["ta_id"]

    extraTA = None

    for ta in ta_schedule:
        if ta["ta_id"] == extraTAId:
            extraTA = deepcopy(ta)
            end_index += 1
            extraTA["ta_id"] = end_index
            break

    ta_schedule.append(extraTA)

    # write_dict_to_json(assignments, "assignment_output_files/check.json")
    write_dict_to_json(ta_schedule, "output_files/ta_schedule.json")

    print("INCREMENTAL DUPLICATION: ")
    print(f"NO OF TAs: {len(ta_schedule)}")