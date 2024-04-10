"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import copy

from ..utils.csvToDict import read_csv_to_dict
from ..utils.dictionaryToJsonFile import write_dict_to_json

from ..config.timeSlotMapping import getTimeSlotMapping
from ..config.daysMapping import getDaysMap


def combine_course_schedules(input_file_path: str = "input_files/class_schedule.csv") -> None:

    """
    This function reads the class schedule.csv file and stores data of each section with required information 
    like slots, crns, instructors, etc. in combined_section_data.json

    Arguments
    ----------
        
    Returned Values
    ----------
    None

    """

    schedule_csv_data = read_csv_to_dict(input_file_path)

    exclude_course_numbers = ["4950", "6950", "5007", "4960", "4960R" "4910"]
    # Capstone Design I - 4910

    count = 1
    all_section_count = 1

    # get Time Slot Encoding
    timeSlots = getTimeSlotMapping()

    final_sections = []
    all_sections = []

    for course in schedule_csv_data:

        timeSlotNum = timeSlots.get(course["BEGIN_TIME"] + "-" + course["END_TIME"], 'NA')

        if course["STATUS"] == "A"  and not timeSlotNum == "Z500" and not timeSlotNum == "NA":
            section = {}
            section["section_id"] = all_section_count
            all_section_count += 1
            section["crn"] = int(course["CRN"])
            course_no = course["SUBJECT"] + course["COURSE_NUMBER"]
            section["course_no"] = course_no
            section["credit_hours"] = int(course["MAX_CREDITS"])
            section["course_long_name"] = course["TITLE_SHORT_DESC"]
            section["ins_fname"] = course["PRIMARY_INSTRUCTOR_FIRST_NAME"] if course["PRIMARY_INSTRUCTOR_FIRST_NAME"] else "TBD"
            section["ins_lname"] = course["PRIMARY_INSTRUCTOR_LAST_NAME"] if course["PRIMARY_INSTRUCTOR_FIRST_NAME"] else "TBD"
            section["lab"] = True if 'L' in course_no else False
            section["enrolled"] = int(course['ACTUAL_ENROLLMENT'])
            section["capacity"] = int(course['MAXIMUM_ENROLLMENT'])
            section["slot"] = []

            for day_key, day_code in getDaysMap().items():
                if course[day_key]:
                    section["slot"].append(day_code + timeSlotNum)

            if course["COURSE_NUMBER"] not in exclude_course_numbers and course["COURSE_NUMBER"][0] not in ['7', '8', '9']:
                final_section = copy.deepcopy(section)
                final_section["section_id"] = count
                count += 1
                final_sections.append(final_section)
            all_sections.append(section)

    # Saving FINAL and ALL Section Data to an output file
    print("Writing FINAL Data to JSON file: ", "output_files/combined_section_data.json")
    print("Total sections added in final data: ", len(final_sections))
    write_dict_to_json(final_sections, "output_files/combined_section_data.json")

    print("Writing FINAL Data to JSON file: ", "output_files/all_section_data.json")
    print("Total sections added in final data: ", len(all_sections))
    write_dict_to_json(all_sections, "output_files/all_section_data.json")
