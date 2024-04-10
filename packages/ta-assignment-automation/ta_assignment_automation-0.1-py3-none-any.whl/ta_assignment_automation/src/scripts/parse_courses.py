"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

from ..utils.csvToDict import read_csv_to_dict
from ..utils.dictionaryToJsonFile import write_dict_to_json

def parseCourses(input_file_path:str ="input_files/class_schedule.csv", output_file_path:str ="output_files/courses.json") -> None:
    
    """
    This function parses the class_schedule CSV file and store the course data in json file

    Arguments
    ----------
    input_file_path: str
        the path clas schedule CSV file
    output_file_path: str
        the path of the json file to store the course data
        
    Returned Values
    ----------
    None

    """
    
    print("Reading Course Data")
    # Read Courses from the csv file and convert it to a dictionary
    courses_init = read_csv_to_dict(input_file_path)

    courses = []
    added_courses_check = set()

    for course in courses_init:

        courseNumber = course['SUBJECT'] + course['COURSE_NUMBER'] # e.g. CSCI8900

        # STATUS == "A" -> Active Courses
        if course['STATUS'] == 'A' and courseNumber not in added_courses_check:
            added_courses_check.add(courseNumber)
            courseLongName = course['TITLE_SHORT_DESC']
            creditHours = int(course['MAX_CREDITS'])

            # Add course to array
            courses.append({"course_no": courseNumber, "course_name": courseLongName, "credit_hours": creditHours})

    # Saving Course Data to output file
    print("Writing Course Data to JSON file: ", output_file_path)
    print("Total Courses added: ", len(added_courses_check))
    write_dict_to_json(courses, output_file_path)

