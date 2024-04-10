"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json

def getCoursesTakenFromCRN(crn_array: list=[]) -> list:

    """
    This utility function returns the list of courses by searching through the section data for the given crn array

    Arguments
    ----------
    crn_array: list
        a list of crns for which you want the correspinding courses
        
    Returned Values
    ----------
    courses: list
        list of courses that correspond to the CRN

    """

    with open("output_files/all_section_data.json", 'r') as file:
        all_sections = json.load(file)

    courses = set()
    for section in all_sections:

        crn = section["crn"]

        if crn in crn_array:
            courses.update([section["course_no"]])
        
    return list(courses)
