"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json

def getTimeSlotsFromCRN(crn_array: list =[]) -> list:

    """
    This utility function returns all the unique time slots that the CRNs have

    Arguments
    ----------
    crn_array: list
        a list of crns for which you want to extract all the time slots
        
    Returned Values
    ----------
    all_slots: list
        list of all unique time slots that are covered by the CRNs

    """

    with open("output_files/all_section_data.json", 'r') as file:
        all_sections = json.load(file)

    # Map the crn to time slots (All time slots will be added to array)
    crn_slot_map = {}

    for section in all_sections:

        crn = section["crn"]

        if crn in crn_slot_map:
            crn_slot_map[crn].extend(section["slot"])
        else:
            crn_slot_map[crn] = section["slot"]
    
    all_slots = set()

    for crn in crn_array:
        if crn in crn_slot_map:
            all_slots.update(crn_slot_map[crn])

    return list(all_slots)