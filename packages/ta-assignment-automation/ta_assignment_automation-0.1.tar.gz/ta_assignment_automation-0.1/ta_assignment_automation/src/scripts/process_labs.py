"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

from ..config.getPseudoLabs import getPseudoLabs
from ..config.lab_ta_requirements import getLabTAReq

def getLabSlots(lab_data: dict) -> dict:
    """
    This function is specifically for labs that have some slots which are non-labs (1730, 3030, 1302)
    and hence can be considered non-relevant for better assignment

    Arguments
    ----------
    lab_data: dict
        Dictionary that maps Course number with array with all sections in it e.g. 
        {
           "CSCI1301L": [{SECTION 1}, {SECTION 2}],
        }
        
    Returned Values
    ----------
    lab_data: list
        the same format as input data but this time the lab and non-lab slots are separated for certain labs
    """

    for lab_course_no, lab_sections in lab_data.items():

        # 1730 and 3030 has two classes on similar timings and one separately which is the lab and we only need to consider that slot during conflict
        if lab_course_no == "CSCI3030" or lab_course_no == "CSCI1730":
            new_lab_sections = []

            for section in lab_sections:

                # It is assumed that it will have 3 slots
                slot = section["slot"]
                section["orig_slot"] = slot

                if slot[0][1:] == slot[1][1:]:
                    section["non_lab_slot"]  = [slot[0], slot[1]]
                    section["slot"] = [slot[2]]
                elif slot[0][1:] == slot[2][1:]:
                    section["non_lab_slot"]  = [slot[0], slot[2]]
                    section["slot"] = [slot[1]]
                else:
                    section["non_lab_slot"]  = [slot[1], slot[2]]
                    section["slot"] = [slot[0]]

                new_lab_sections.append(section)

            lab_data[lab_course_no] = new_lab_sections

    return lab_data
            
def mergedCrnsBasedOnRequirement(lab_data: dict) -> list:
    """
    This function takes lab data dictionary as argument and returns list of labs after merging the CRNs based on the requirement.

    Arguments
    ----------
    lab_data: dict
        Dictionary that maps Course number with array with all sections in it e.g. 
        {
           "CSCI1301L": [{SECTION 1}, {SECTION 2}],
        }
        
    Returned Values
    ----------
    labs: list
        list of all labs after merging them
    """

    lab_ta_req = getLabTAReq()

    for lab_course_no, lab_sections in lab_data.items():

        cut_size = lab_ta_req[lab_course_no]

        new_lab_sections = []

        i = 0
        n = len(lab_sections)
        while i < n:
            j = cut_size
            merged_crns = {}
            while i < n and j > 0:

                if len(merged_crns.keys()) == 0:
                    merged_crns = lab_sections[i]
                    merged_crns["instructors"] = set()
                    ins = lab_sections[i]["ins_fname"] + " " + lab_sections[i]["ins_lname"]
                    merged_crns["instructors"].add(ins)
                else:
                    merged_crns["crn"].extend(lab_sections[i]["crn"])
                    merged_crns["enrolled"] += lab_sections[i]["enrolled"]
                    merged_crns["capacity"] += lab_sections[i]["capacity"]
                    merged_crns['slot'].extend(lab_sections[i]["slot"])
                    if "non_lab_slot" in merged_crns:
                        merged_crns["non_lab_slot"].extend(lab_sections[i]["non_lab_slot"])
                        merged_crns["orig_slot"].extend(lab_sections[i]["orig_slot"])
                    merged_crns["instructors"].add(lab_sections[i]["ins_fname"] + " " + lab_sections[i]["ins_lname"])

                j -= 1
                i += 1
            new_lab_sections.append(merged_crns)
        
        lab_data[lab_course_no] = new_lab_sections

        labs = [lab for final_lab_sections in lab_data.values() for lab in final_lab_sections]

    return labs


def merge1302Sections(lab_data: dict) -> dict:
    """
    This function is specifically created to merge the 1302 sections. Since there are 5 TAs for 6 sections, we merge the section with 
    lowest two enrolments into one (sorting and merging)

    Arguments
    ----------
    lab_data: dict
        Dictionary that maps Course number with array with all sections in it e.g. 
        {
           "CSCI1301L": [{SECTION 1}, {SECTION 2}],
        }
        
    Returned Values
    ----------
    lab_data: dict
        original input dictionary with merged sections for 1302
    """

    section1302 = lab_data["CSCI1302"]

    section1302 = sorted(section1302, key=lambda d: d['enrolled'])

    newDict = section1302[0]
    newDict["crn"].extend(section1302[1]["crn"])
    newDict["enrolled"] += section1302[1]["enrolled"]
    newDict["capacity"] += section1302[1]["capacity"]
    newDict['slot'].extend(section1302[1]["slot"])
    newDict["instructors"] = set()
    ins1 = section1302[0]["ins_fname"] + " " + section1302[0]["ins_lname"]
    ins2 = section1302[1]["ins_fname"] + " " + section1302[1]["ins_lname"]
    newDict["instructors"].add(ins1)
    newDict["instructors"].add(ins2)

    new_section1302 = [newDict]
    new_section1302.extend(section1302[2:])

    lab_data["CSCI1302"] = new_section1302

    return lab_data

def getAllLabs(sections: list) -> list:
    """
    This function takes section as input and returns the required lab data array

    Arguments
    ----------
    sections: list
        list of all sections with merged CRNs
        
    Returned Values
    ----------
    labs: list
        list of all labs
    unique_labs: set
        set of all the lab course numbers
    """

    print("Processing Lab Data")

    pseudo_labs = getPseudoLabs()

    unique_labs = set(section["course_no"] for section in sections if section["lab"] or section["course_no"] in pseudo_labs)

    # Dictionary that maps Course number with array with all sections in it e.g. 
    # {
    #    "CSCI1301L": [{SECTION 1}, {SECTION 2}],
    # }
    lab_data_init = {}

    for section in sections:
        if section["lab"] or section["course_no"] in pseudo_labs:
            if section["course_no"] not in lab_data_init.keys():
                lab_data_init[section["course_no"]] = []
            lab_data_init[section["course_no"]].append(section)

    lab_data = getLabSlots(lab_data_init)

    lab_data = merge1302Sections(lab_data)
    # merge1302Sections(lab_data)

    labs = mergedCrnsBasedOnRequirement(lab_data)

    return labs, unique_labs
