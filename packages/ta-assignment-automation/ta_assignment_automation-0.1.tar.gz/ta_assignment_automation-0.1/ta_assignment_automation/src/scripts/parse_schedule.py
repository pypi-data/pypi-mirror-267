"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

from ..utils.csvToDict import read_csv_to_dict
from ..utils.dictionaryToJsonFile import write_dict_to_json
from ..config.timeSlotMapping import getTimeSlotMapping
from ..config.daysMapping import getDaysMap


def parseSchedule(input_file_path:str ="input_files/class_schedule.csv", output_file_path :str ="output_files/schedule.json") -> None:
    
    """
    This function parses class schedule and creates the schedule.json file with all the schedule information.
    Schedule is an atomic unit with each CRN mapped to one time slot based on the time slot mapping file

    Arguments
    ----------
    input_file_path: str
        the path to the class schedule CSV file
    output_file_path: str
        the path of the json file to store the class schedules
        
    Returned Values
    ----------
    None

    """
    
    print("Reading Course Data to Add Schedule")
    # Read Courses from the csv file and convert it to a dictionary
    courses_init = read_csv_to_dict(input_file_path)

    # Store all schedule data
    schedules = []

    # get Time Slot Encoding
    timeSlots = getTimeSlotMapping()

    count = 1

    for course in courses_init:
        if course['STATUS'] == 'A':

            # TIME SLOTS - map the slots using the dictionary
            timeSlotNum = timeSlots.get(course["BEGIN_TIME"] + "-" + course["END_TIME"], 'NA')

            # Add the crn with time 00:00 - 11:59 directly since they don't require classroom and do not have a specific day
            if timeSlotNum == "Z500":
                schedule = {}
                schedule["schedule_id"] = count
                count += 1
                schedule["crn"] = int(course["CRN"])
                schedule["slot"] = timeSlotNum
                schedules.append(schedule)

            slotted_schedules = []

            for day_key, day_code in getDaysMap().items():
                if course[day_key]:
                    schedule = {}
                    schedule["schedule_id"] = count
                    count += 1
                    schedule["crn"] = int(course["CRN"])
                    schedule["slot"] = day_code + timeSlotNum
                    slotted_schedules.append(schedule)

            for scheds in slotted_schedules:
                schedules.append(scheds)

    # Saving Section Data to an output file
    print("Writing Schedule Data to JSON file: ", output_file_path)
    print("Total Schedule added: ", len(schedules))
    write_dict_to_json(schedules, output_file_path)
