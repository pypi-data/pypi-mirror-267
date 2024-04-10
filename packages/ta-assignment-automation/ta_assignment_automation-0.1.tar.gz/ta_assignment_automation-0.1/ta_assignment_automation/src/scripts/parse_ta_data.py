"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

from ..utils.csvToDict import read_csv_to_dict
from ..utils.dictionaryToJsonFile import write_dict_to_json
from ..utils.filterDigits import filter_digits
from ..scripts.getTimeSlotsFromCRN import getTimeSlotsFromCRN
from ..scripts.getCoursesTakenFromCrn import getCoursesTakenFromCRN

def parseTAData(input_file_path:str ="input_files/TA_schedule.csv", output_file_path:str ="output_files/ta_schedule.json") -> None:
    
    """
    This function parses the TA schedule and stores it to a json file

    Arguments
    ----------
    input_file_path: str
        the path to the TA schedule CSV file
    output_file_path: str
        the path of the json file to store the TA schedules
        
    Returned Values
    ----------
    None

    """

    print("Reading TA Data")
    # Read Courses from the csv file and convert it to a dictionary
    ta_csv_data = read_csv_to_dict(input_file_path)

    ta_schedule = []

    count = 1

    for ta in ta_csv_data:

        ta_data = {}

        if '@' not in ta['UGAEmail'] or ta["hours"] == "IoR":
            continue
        
        ta_data["ta_id"] = count
        count += 1
        ta_data["UGAID"] = ta["UGAID"]
        ta_data["email"] = ta["UGAEmail"]
        ta_data["fname"] = ta["FirstName"]
        ta_data["lname"] = ta["LastName"]
        ta_data["hours"] = ta["hours"]

        # This is only for the combined view - we need a different way to keep schedules
        if ta["CRNs"]:
            crns = filter_digits(ta["CRNs"].split(","))
            ta_data["crns"] = crns
            ta_data["slots"]  = getTimeSlotsFromCRN(crns) # slots will be empty array if it is a non CSCI course or course like directed study
            ta_data["courses_taken"] = getCoursesTakenFromCRN(crns)
        ta_schedule.append(ta_data)

    # Saving Course Data to output file
    print("Writing TA Data to JSON file: ", output_file_path)
    print("Total TAs added: ", len(ta_schedule))
    write_dict_to_json(ta_schedule, output_file_path)

