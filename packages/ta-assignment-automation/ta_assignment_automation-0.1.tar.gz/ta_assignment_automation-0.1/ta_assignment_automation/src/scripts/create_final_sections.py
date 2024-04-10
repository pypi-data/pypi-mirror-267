"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import json
import copy

from ..config.getPseudoLabs import getPseudoLabs
from ..config.capacity_cap import getCapacityCap

from ..scripts.process_labs import getAllLabs

def combineSectionWithSameCRN(input_file_path: str) -> list:

    """
    This functions merges all sections that have the same CRN

    Arguments
    ----------
    input_file_path: str
        the path to combined section data
        
    Returned Values
    ----------
    sections: list
        list of sections with same CRNs merged together

    """

    print("READING COMBINED SECTION DATA")
    # Fetch All combined  section data
    combined_sections = json.load(open(input_file_path))

   # Merge all sections with same CRN
    sections = []
    crns = {}

    for section in combined_sections:
        if section["crn"] not in crns.keys():
            crns[section["crn"]] = section
        else:
            crns[section["crn"]]["slot"].extend(section["slot"])
            # At this point they are the same CRN, so capacity and enrolled will remain the same
            # crns[section["crn"]]["enrolled"] += section["enrolled"]

    for _,section in crns.items():
        section["crn"] = [section["crn"]]
        sections.append(section)
    return sections

def mergeFourAndSixSectionsTogether(sections: list) -> tuple:
    
    """
    This function merges the 4000 -level section with corresponding 6000 level section if it is under the same instructor

    Arguments
    ----------
    sections: list
        List of sections with separate 4/6000-level sections
        
    Returned Values
    ----------
    (FourZeroSectionsOfSameIns, X0Classes_dont_add) : tuple
        A tuple with Dictionary of 4000 level classes with correspoinding 6000 level class merged together and 
        the set of keys of 6000 level class to exclude while making final sections

    """

    FourZeroSectionsOfSameIns = {} # All classes with CSCI4xxx course number
    X0Classes_dont_add = set() # put the CSCI6xxxx course that have a 4xxx here, so that we don't have duplicates

    for section in sections:
        if not section["lab"]:
            key = section["course_no"] + "_" + section["ins_fname"] + "_" + section["ins_lname"]

            if key.startswith("CSCI4"):
                if key in FourZeroSectionsOfSameIns.keys():
                    FourZeroSectionsOfSameIns[key].append(section)
                else:
                    FourZeroSectionsOfSameIns[key] = [section]

    for section in sections:
        if not section["lab"]:
            key = section["course_no"] + "_" + section["ins_fname"] + "_" + section["ins_lname"]
            if key.startswith("CSCI6"):
                counter_part = key[:4]  + '4' + key[5:]
                if counter_part in FourZeroSectionsOfSameIns.keys():
                    X0Classes_dont_add.add(key)
                    FourZeroSections = FourZeroSectionsOfSameIns[counter_part]
                    for i in range(len(FourZeroSections)):
                        if sorted(FourZeroSections[i]["slot"]) == sorted(section["slot"]):
                            FourZeroSectionsOfSameIns[counter_part][i]["crn"].extend(section["crn"])
                            FourZeroSectionsOfSameIns[counter_part][i]["enrolled"] += (section["enrolled"])
                            FourZeroSectionsOfSameIns[counter_part][i]["capacity"] += (section["capacity"])
                            

    return FourZeroSectionsOfSameIns, X0Classes_dont_add

def processFinalSections(sections: list, labs: list, lab_cno: set, FourZeroSectionsOfSameIns: dict, X0Classes_dont_add: set) -> list:
    """
    This function creates the final sections data which means it merges all the CRNs and the slots of the sections into a final sections. 
    It also stores the labs and non lab courses separately.
    It also merges classes that are 4/6000 levels based on the time slots.

    Arguments
    ----------
    sections: list
        list of all sections with merged CRNs
    labs: list
        list of all labs with merged CRNs
    lab_cno: set
        set of all lab course numbers (includes pseudo_labs)
    FourZeroSectionsOfSameIns: dict
        dictionary of 4000 level classes with correspoinding 6000 level class merged together
    X0Classes_dont_add: set
        the set of keys of 6000 level class to exclude while making final sections
        
    Returned Values
    ----------
    final_sections: list
        list of final sections to be saved to file
    """

    semi_final_sections = []

    for lab in labs:
        if "instructors" in lab:
            lab["instructors"] = list(lab["instructors"])
        semi_final_sections.append(lab)

    for section in sections:
        key = section["course_no"] + "_" + section["ins_fname"] + "_" + section["ins_lname"]

        if section["course_no"] in lab_cno:
            continue

        if key in X0Classes_dont_add:
            continue
        if key in FourZeroSectionsOfSameIns.keys():
            fsections = FourZeroSectionsOfSameIns[key]
            for fsection in fsections:
                if sorted(fsection["slot"]) == sorted(section["slot"]):
                    semi_final_sections.append(fsection)
        else:
            semi_final_sections.append(section)

    index = 1
    
    final_sections = []

    courses_to_exclude = ["CSCI1301", "CSCI2150", "CSCI4830", "CSCI4900"]
    # PROVIDE INDEX AND REMOVE SECTIONS WITH ENROLLMENT LESS THAN 20 (Less than 1/2 TA requirement)
    for section in semi_final_sections:

        if section["course_no"] in courses_to_exclude:
            continue
        if section["enrolled"] > getCapacityCap()[0.5]:
            section["section_id"] = index
            index += 1
            final_sections.append(section)
        # If they have more than 80 students (capacity cap - 2 -> two TAs required to handle this class)
        # By adding this number of section increased from 79 -> 87 (95 if we allowed this for labs)
        if section["enrolled"] > getCapacityCap()[2] and not section["course_no"] in lab_cno:
            new_section = copy.deepcopy(section)
            new_section["section_id"] = index
            index += 1
            final_sections.append(new_section)

    return final_sections


def create_final_sections(input_file_path:str ="output_files/combined_section_data.json", output_file_path: str="output_files/section_data") -> None:
    
    """
    This function creates the final sections data which means it merges all the CRNs and the slots of the sections into a final sections. 
    It also stores the labs and non lab courses separately.
    It also merges classes that are 4/6000 levels based on the time slots.

    Arguments
    ----------
    input_file_path: str
        the path to combined section data
    output_file_path: str
        the path to the folder where you want to store the section, lab and non_lab data
        
    Returned Values
    ----------
    None

    """
    
    sections = combineSectionWithSameCRN(input_file_path)

    labs, lab_cno = getAllLabs(sections)

    FourZeroSectionsOfSameIns, X0Classes_dont_add = mergeFourAndSixSectionsTogether(sections)

    final_sections = processFinalSections(sections, labs, lab_cno ,FourZeroSectionsOfSameIns, X0Classes_dont_add)

    print("SAVING SECTION, LAB AND NON-LAB DATA INTO JSON FILES. OUTPUT FOLDER: ", output_file_path)

    with open(f"{output_file_path}/section.json", "w") as f:
        json.dump(final_sections,f)

    print("NO OF TOTAL SECTIONS", len(sections))
    print("NO OF FINAL SECTIONS", len(final_sections))

