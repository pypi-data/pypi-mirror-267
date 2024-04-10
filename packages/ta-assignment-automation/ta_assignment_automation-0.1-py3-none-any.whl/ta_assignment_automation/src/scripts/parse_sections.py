"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

from ..utils.csvToDict import read_csv_to_dict
from ..utils.dictionaryToJsonFile import write_dict_to_json

def parseSections(input_file_path:str ="input_files/class_schedule.csv", output_file_path:str ="output_files/sections.json") -> None:
    
    """
    This function parses the class schedule and extracts the section information and then stores it to a json file

    Arguments
    ----------
    input_file_path: str
        the path to the class schedule CSV file
    output_file_path: str
        the path of the json file to store the sections
        
    Returned Values
    ----------
    None

    """
    
    print("Reading Course Data to Add Sections")
    # Read Courses from the csv file and convert it to a dictionary
    courses_init = read_csv_to_dict(input_file_path)

    # Store all section data
    sections = []
    unique_sections = []
    u_crn = set()

    for course in courses_init:
        if course['STATUS'] == 'A':

            section = {}
            section["crn"] = int(course["CRN"])
            course_no = course['SUBJECT'] + course['COURSE_NUMBER']
            section["course_no"] = course_no
            section["lab"] = True if 'L' in course_no else False
            section["ins_fname"] = course["PRIMARY_INSTRUCTOR_FIRST_NAME"] if course["PRIMARY_INSTRUCTOR_FIRST_NAME"] else "TBD"
            section["ins_lname"] = course["PRIMARY_INSTRUCTOR_LAST_NAME"] if course["PRIMARY_INSTRUCTOR_FIRST_NAME"] else "TBD"
            section["enrolled"] = int(course['ACTUAL_ENROLLMENT'])
            section["capacity"] = int(course['MAXIMUM_ENROLLMENT'])

            sections.append(section)

            if not int(course["CRN"]) in u_crn:
                u_crn.add(int(course["CRN"]))
                unique_sections.append(section)

    # Saving Section Data to an output file
    print("Writing Section Data to JSON file: ", output_file_path)
    print("Total Sections added: ", len(sections))
    write_dict_to_json(sections, output_file_path)
    write_dict_to_json(unique_sections, "/".join(output_file_path.split("/")[:-1]) + "/unique_sections.json")
