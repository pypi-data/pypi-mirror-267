"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json
from copy import deepcopy

from ..config.capacity_cap import getCapacityCap
from ..utils.dictionaryToJsonFile import write_dict_to_json

def duplicateTAs() -> None:

    """
    This function creates duplicate TAs in TA_schedule.json from the TAs that have been assigned to class with 0.5 TA requirement

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

    with open("assignment_output_files/unassigned_courses.json", 'r') as file:
        unassigned = json.load(file)
    
    if len(unassigned) == 0:
        return

    end_index = max(ta["ta_id"] for ta in ta_schedule) # get the last id

    print("TOTAL TAs before Duplication: ", len(ta_schedule))

    ta_ids_to_dupe = []

    # Get the IDs of the TAs that we need to duplicate
    for assignment in assignments:
        if assignment["enrolled"] < getCapacityCap()[1]:
            ta_ids_to_dupe.append(assignment["ta_id"])
    
    dupe_tas = []

    for ta in ta_schedule:
        if ta["ta_id"] in ta_ids_to_dupe:
            ta_data = deepcopy(ta)
            end_index += 1
            ta_data["ta_id"] = end_index
            dupe_tas.append(ta_data)
    

    for ta in dupe_tas:
        ta_schedule.append(ta)

    write_dict_to_json(ta_schedule, "output_files/ta_schedule.json")

    print("TOTAL TAs after Duplication: ")
    print(len(ta_schedule))
    print()
