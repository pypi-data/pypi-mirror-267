"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json

def showAssignments(job_cost: list, cost_matrix: list, ta_data_file_path:str ="output_files/ta_schedule.json", section_file_path:str ="output_files/section_data/section.json", output_folder_path:str ="assignment_output_files/", showLogs: bool = True) -> None:

    """
    This utility function prints out the results of the TA assignements

    Arguments
    ----------
    job_cost: list
        the list of TAs
    cost_matrix
        list of cost is an numpy.ndarray that stores the cost of assigning the TAs to the courses.
    ta_data_file_path: str
        the path to the TA schedule CSV file
    section_file_path: str
        the path to the section json file
    output_folder_path: str
        the path to the folder where you want to store the TA assignments and the unassigned courses
    showLogs: bool
        flag -> if you do not wish print the assignments (set to False)
        defaule value => True

    Returned Values
    ---------------
    None

    """

    job, acost = job_cost

    assignments = []
    unassignedCourses = []

    json_filename = 'ta_assignments.json'

    with open(section_file_path, 'r') as file:
        sections = json.load(file)

    with open(ta_data_file_path, 'r') as file:
        ta_schedule = json.load(file)
    
    ta_data = {int(ta["ta_id"]): ta for ta in ta_schedule}
    course_data = {int(section["section_id"]): section for section in sections}

    assignmentIndex = 1

    for w in range(len(job)-1):
        j = job[w]
        if job[w] != -1:
            cost_str = str(cost_matrix[j][w])
        else:
            cost_str = "NA"
        if showLogs:
            print(f"job {j} assigned to worker {w} with cost (j = {j}, w = {w}) = {cost_str}")
        if not "instructors" in course_data[w+1].keys():
            course_data[w+1]['instructors'] = []
        if j != -1:
            # print(f"TA {j+1}  : | { ta_data[j+1]['fname'] + ta_data[j+1]['lname']} | assigned to Course {w+1}:  | {course_data[w+1]['course_no']} with CRN: {course_data[w+1]['crn']} under instructor {course_data[w+1]['ins_fname']} {course_data[w+1]['ins_lname']}   | with cost (j = {j}, w = {w}) = {cost_str}")
            assignments.append(
                {
                    'assignmentId': assignmentIndex,
                    'ta_id': ta_data[j+1]['ta_id'], 
                    'uga_id': ta_data[j+1]['UGAID'],
                    'email': ta_data[j+1]['email'],
                    'fname': ta_data[j+1]['fname'], 
                    'lname': ta_data[j+1]['lname'],
                    'course_no': course_data[w+1]['course_no'],
                    'crn': course_data[w+1]['crn'],
                    'section_id': course_data[w+1]['section_id'],
                    'ins_fname': course_data[w+1]['ins_fname'],
                    'ins_lname': course_data[w+1]['ins_lname'],
                    'instructors': course_data[w+1]['instructors'],
                    'course_name': course_data[w+1]['course_long_name'],
                    'lab': course_data[w+1]['lab'],
                    'cost': cost_str,
                    'enrolled': course_data[w+1]['enrolled'],
                    'capacity': course_data[w+1]['capacity'],
                    'ta_hours': float(ta_data[j+1]['hours']),
                })
            assignmentIndex += 1   
        else:
            if showLogs:
                print(f"No TAs assigned to Course {w+1}:  | {course_data[w+1]['course_no']} with CRN: {course_data[w+1]['crn']} under instructor {course_data[w+1]['ins_fname']} {course_data[w+1]['ins_lname']} with cost (j = {j}, w = {w}) = {cost_str}")
            unassignedCourses.append(course_data[w+1])

    with open(output_folder_path + json_filename, 'w') as json_file:
        json.dump(assignments, json_file, indent=2)
    with open(output_folder_path + "unassigned_courses.json", 'w') as j_file:
        json.dump(unassignedCourses, j_file, indent=2)

    
    print(f"accumulating costs: {acost}")

    print("\n\n------------------------------------------------\n\n")

    print("TOTAL TA assigned: ",len(assignments))
    print("TOTAL Unassigned Classes: ",len(unassignedCourses))

    if len(unassignedCourses) > 0:
        print("\n\n------------------------------------------------\n\nUnassigned courses: ")
        unIndex = 1
        for course in unassignedCourses:
            course_no = course["course_no"]
            isLab = course["lab"]
            course_long_name = course["course_long_name"]
            print(f"{unIndex}. {course_no} | Lab = {isLab} | NAME: {course_long_name}")
            unIndex += 1