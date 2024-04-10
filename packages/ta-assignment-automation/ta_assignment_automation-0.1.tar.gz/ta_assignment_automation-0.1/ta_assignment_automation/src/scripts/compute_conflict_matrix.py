"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json

from ..config.edgeWeights import getEdgeWeights
from ..config.getPseudoLabs import getPseudoLabs
from ..config.capacity_cap import getCapacityCap

from ..utils.saveMatirxToTxtFile import saveMatToTxt

from .create_conflict_breakdown_skeleton import createConflictBreakdownSkeleton

def computeConflictMatrix(output_file_path:str ="output_files/conflict_matrix.json") -> None:

    """
    This function computes the conflict matrix which is a matrix that stores the number of conflicts
    the TAs have with the Sections. It then calls the saveConflictMatrix function to save the generated matrix into a text file
    It takes data from section, TA schedules and Instructor Preference json files

    Arguments
    ----------
    output_path: str
        the path to the json file where you want to store the conflict matrix
        
    Returned Values
    ----------
    None

    """

    # Initialise Conflict BreakDown Matrix
    conflict_breakdown = createConflictBreakdownSkeleton()

    # with open("output_files/combined_section_data.json", 'r') as file:
    #     sections = json.load(file)

    with open("output_files/section_data/section.json", 'r') as file:
        sections = json.load(file)

    with open("output_files/ta_schedule.json", 'r') as file:
        ta_schedule = json.load(file)

    with open("output_files/ins_pref.json", 'r') as file:
        ins_pref_data = json.load(file)

    edgeWeights = getEdgeWeights()
    pseudo_labs = getPseudoLabs()

    conflict_matix = {}

    for ta in ta_schedule:

        ta_id = ta["ta_id"]
        ta_email = ta["email"]
        ta_slots = set(ta["slots"])
        ta_crns = ta["crns"]
        ta_courses = ta["courses_taken"]

        for section in sections:

            section_id = section["section_id"]
            # crn = section["crn"]
            course_no = section["course_no"]
            # slots = set(section["slot"])
            ins_pref_key = section["course_no"] + section["ins_lname"]
            
            value = 0

            # compute value based on weights
            # 1. Time conflict
            # if len(slots.intersection(ta_slots))  > 0 and section["lab"]:
            #     value += edgeWeights["time_conflict"]
            if section["lab"] or (section["course_no"] in pseudo_labs):
                for slot in section["slot"]:
                    if slot in ta_slots:
                        cost = edgeWeights["time_conflict"]
                        value += cost
                        conflict_breakdown[ta_id][section_id]["time_conflict_with_lab"] += cost

                # TODO - ASK THE GRAD COORDINATORS
                # only 18 hr TA should be assigned to one-one labs with lots of students
                if section["enrolled"] > getCapacityCap()[2] and ta["hours"] == "13.33": 
                # if section["course_no"] == "CSCI1302" and ta["hours"] == "13.33":
                    cost = 50
                    value += cost
                    conflict_breakdown[ta_id][section_id]["ta_hours_less_class_has_more_capacity"] += cost
                    

            # 2. TA is currently taking this course - number of CRN = number of conflicts x weight for class conflict
            if course_no in ta_courses:
                cost = (len(section["crn"]) * edgeWeights["current_course"])
                value += cost #  ABSOLUTE NO -> CANNOT ALLOW
                conflict_breakdown[ta_id][section_id]["ta_currently_taking_this_class"] += cost
            
            # 3. TA did not "TA" for this class before
            # TODO - we do not have the data at present

            # 4. Not in the preference list of the instructor for this course
            if ins_pref_key in ins_pref_data:
                if (not "pref1" in ins_pref_data or ins_pref_data[ins_pref_key]["pref1"] != ta_email) and (not "pref2" in ins_pref_data or ins_pref_data[ins_pref_key]["pref2"] != ta_email):
                    cost = edgeWeights["not_ins_pref"]
                    value += cost
                    conflict_breakdown[ta_id][section_id]["not_instructor_preference"] += cost
                    # value += (len(section["crn"]) * edgeWeights["not_ins_pref"])
                elif "pref1" in ins_pref_data and ins_pref_data[ins_pref_key]["pref1"] != ta_email:
                    cost = edgeWeights["not_first_pref"]
                    value += cost
                    conflict_breakdown[ta_id][section_id]["not_instructor_first_preference"] += cost
                    # value += (len(section["crn"]) * edgeWeights["not_first_pref"])

            # 5. TA did not take this course before
            # TODO - we do not have the data at present

            # 6. TA is not available during class time
            # if len(slots.intersection(ta_slots))  > 0 and not section["lab"]:
            #     value += edgeWeights["not_avail_at_class_time"]
            if not section["lab"]:
                for slot in section["slot"]:
                    if slot in ta["slots"]:
                        cost = edgeWeights["not_avail_at_class_time"]
                        value += cost
                        conflict_breakdown[ta_id][section_id]["not_avaliable_at_class_time"] += cost

            if ta_id not in conflict_matix:
                conflict_matix[ta_id] = {}
            
            # Add value to matrix
            conflict_matix[ta_id][section_id] = value
            conflict_breakdown[ta_id][section_id]["total_cost"] = value

    # Save matrix to JSON file
    with open(output_file_path, 'w') as json_file:
        json.dump(conflict_matix, json_file, indent=4)
    print("CONFLICT MATRIX JSON MAPPING SAVED TO: ", output_file_path)

    with open("assignment_output_files/cost_break_down.json", "w") as json_file:
        json.dump(conflict_breakdown, json_file, indent=4)
    print("CONFLICT BREAKDOWN MATRIX SAVED TO: assignment_output_files/cost_break_down.json")

    saveMatToTxt(conflict_matix)
    


