"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json
from copy import deepcopy

def getDuplicateTAs(ta_assignments: list) -> set:
    """
    This function returns the set of all TA emails that are duplicate -> Assigned to 2 classes

    Arguments
    ----------
    ta_assignments: list
        List of all the TA assignments

    Returned Values
    ---------------
    dupeTAEmails: set
        Set of all TAs who have been assigned to 2 classes

    """
    dupeTAEmails = set()
    allTAEmails = set()

    for assignment in ta_assignments:
        email = assignment["email"]

        if email in allTAEmails:
            dupeTAEmails.add(email)
        allTAEmails.add(email)

    return dupeTAEmails

def splitTAhours(input_file_path:str ="assignment_output_files/ta_assignments.json") -> None:

    """
    This function splits TA hours based on the enrollment ratio, if they are assigned to more than one section

    Arguments
    ----------
    input_folder: str
        The path to the Assignment file

    Returned Values
    ---------------
    None

    """

    with open(input_file_path, 'r') as file:
        ta_assignments = json.load(file)

    # Get teh set of ALL TA's who have been assigned to 2 classes
    dupeTAEmails = getDuplicateTAs(ta_assignments)

    print("DUPLICATE TAs\n------------------------------------------------")
    for email in dupeTAEmails:
        print(email)
    print("------------------------------------------------")

    dualTAs = {}

    for assignment in ta_assignments:
        email = assignment["email"]
        if email in dupeTAEmails:
            if email not in dualTAs.keys():
                dualTAs[email] = []
            dualTAs[email].append(assignment)

    updated_assignements = {}

    for _, ta_class in dualTAs.items():
        ta_hours = ta_class[0]["ta_hours"]
        total_enrollment = ta_class[0]["enrolled"] + ta_class[1]["enrolled"]
        ta_class[0]["ta_hours"] = round(float(ta_class[0]["enrolled"] / total_enrollment) * ta_hours, 2)
        ta_class[1]["ta_hours"] = round(float(ta_class[1]["enrolled"] / total_enrollment) * ta_hours, 2)
        updated_assignements[ta_class[0]["assignmentId"]] = ta_class[0]
        updated_assignements[ta_class[1]["assignmentId"]] = ta_class[1]

    copyOfAssignments = []

    for assignment in ta_assignments:
        if assignment["assignmentId"] in updated_assignements:
            assignment = deepcopy(updated_assignements[assignment["assignmentId"]])
        copyOfAssignments.append(assignment)
    
    with open(input_file_path, 'w') as json_file:
        json.dump(copyOfAssignments, json_file, indent=2)