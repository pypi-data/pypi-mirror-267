"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json
from copy import deepcopy


def createConflictBreakdownSkeleton()-> dict:
    """
    This function creates the skeleton for conflict break down matrix.
    This matrix maps TA to Sections with the conflicts and contains information the cost based on different criteria

    EXAMPLE STRUCTURE:

    This json data will have TA id mapped to all the sections and each section they will have the criteria detail 
    and the cost associated with it

    {
        "total_ta": 64,               // total number of TAs
        "total_sections": 64,         // total number of sections
        "1": {                        // TA ID 
            "ta_id": 1,
            "fname": "Yulong ",
            "lname": "Wang",
            "email": "yw98883@uga.edu",         // REQUIRED DETAILS OF TA
            "1": {                              // SECTION DATA
                "section_id": 1,
                "course_no": "CSCI3030",
                "course_long_name": "Computing Ethics and Society",
                "total_cost": 4,
                "time_conflict_with_lab": 0,
                "ta_hours_less_class_has_more_capacity": 0,             // CRITERIA FOR CONFLICT
                "ta_currently_taking_this_class": 0,
                "not_instructor_preference": 4,
                "not_instructor_first_preference": 0,
                "did_not_TA_this_class_before": 0,
                "did_not_take_this_class_before": 0,
                "not_avaliable_at_class_time": 0
            },
    }

    Arguments
    ----------
    None
    
    Returned Values
    ----------
    conflit_breakdown_matix: dict
        This dictionary maps TA with Sections with the cost breakdown

    """

    # cost breakdown initialization
    cost_breakdown = {
        "total_cost": 0,
        "time_conflict_with_lab": 0,
        "ta_hours_less_class_has_more_capacity": 0,
        "ta_currently_taking_this_class":0,
        "not_instructor_preference": 0,
        "not_instructor_first_preference": 0,
        "did_not_TA_this_class_before": 0,
        "did_not_take_this_class_before":0,
        "not_avaliable_at_class_time": 0
    }

    with open("output_files/section_data/section.json", 'r') as file:
        sections = json.load(file)

    with open("output_files/ta_schedule.json", 'r') as file:
        ta_schedule = json.load(file)

    section_data = {}

    # Add section data with cost breakdown skeleton
    for section in sections:
        section_data[section["section_id"]] = {
            "section_id": section["section_id"],
            "course_no": section["course_no"],
            "course_long_name": section["course_long_name"],
        }

        section_data[section["section_id"]].update(deepcopy(cost_breakdown))

    conflict_breakdown = {
        "total_ta": len(ta_schedule),
        "total_sections": len(sections)
    }

    for ta in ta_schedule:
        
        conflict_breakdown[ta["ta_id"]] = {
            "ta_id": ta["ta_id"],
            "fname": ta["fname"],
            "lname": ta["lname"],
            "email": ta["email"],
        }

        conflict_breakdown[ta["ta_id"]].update(deepcopy(section_data))

    print("Conflict Breakdown Matrix initialised")
    with open("assignment_output_files/cost_break_down.json", "w") as json_file:
        json.dump(conflict_breakdown, json_file, indent=4)
    print("CONFLICT BREAKDOWN MATRIX SAVED TO: assignment_output_files/cost_break_down.json")

    return conflict_breakdown