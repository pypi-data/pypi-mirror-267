"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

from ..utils.csvToDict import read_csv_to_dict
from ..utils.dictionaryToJsonFile import write_dict_to_json

def parseInstructorPref(input_file_path:str ="input_files/Instr_Pref.csv", output_file_path:str ="output_files/ins_pref.json") -> None:

    """
    This function parses the Instructor preference and store that in a json file
    
    If you look at the code, for some of the classes starting with CSCI4, 
    we are assigning instructor preference to their 6000-level class as well.

    For example, Instructor for CSCI 4050 will have their preference for that class,
    but the instructor teaches both 4050 and 6050 but in the preference file it will be mentioned as 4050.
    So we assign the preference to equivalend 6000 level class as well which in this case is 6050

    Now if an instructor has preference for the 6000 level class (grad-only), then we will only create prefence for that class.
    Because the key we generate will only assign the preference if the instructor takes both the class, otherwise it will
    assign preference to 4000 level and 6000 level separately.


    Arguments
    ----------
    input_file_path: str
        the path to the instructor preference CSV file
    output_file_path: str
        the path of the json file to store the instructor prefrence data
        
    Returned Values
    ----------
    None

    """

    pref_data = read_csv_to_dict(input_file_path)

    # Map ta by email to a dictonary
    # CSCI4050Saleh: {
    #  course_no: "CSCI4050",
    #   ins_lname: "Saleh",
    #   pref1: "email1"
    #   pref2: "email2"
    # }
    # 

    inst_pref = {}

    for row in pref_data:
        if row["Email"] and row["pref"] and not row["pref"].strip() == "---":
            ins_course_list = [p.strip() for p in row["pref"].split(";")]

            ta_email = row["Email"]

            for ins_course in ins_course_list:
                if len(ins_course) > 0 and ins_course[0] != '':
                    course_no = "CSCI"+ins_course.split("/")[1]
                    ins_lname = ins_course.split("/")[0].split("(")[0]
                    pref_num = ins_course.split("/")[0].split("(")[1][0]

                    ins_pref_key = course_no + ins_lname
                    ins_pref_grad_key = "CSCI6" + course_no[1:] + ins_lname

                    if ins_pref_key not in inst_pref:
                        inst_pref[ins_pref_key] = {}
                    if course_no[0] == '4':
                        inst_pref[ins_pref_grad_key] = {}

                    inst_pref[ins_pref_key]["ins_lname"] = ins_lname
                    inst_pref[ins_pref_key]["pref" + pref_num] = ta_email
                    inst_pref[ins_pref_key]["course_no"] = course_no

                    if course_no[0] == '4':
                        inst_pref[ins_pref_grad_key]["ins_lname"] = ins_lname
                        inst_pref[ins_pref_grad_key]["pref" + pref_num] = ta_email
                        inst_pref[ins_pref_grad_key]["course_no"] = "CSCI6" + course_no[1:]

    # Saving Course Data to output file
    print("Writing Ins Pref Data to JSON file: ", output_file_path)
    print("Total preferences added: ", len(inst_pref))
    write_dict_to_json(inst_pref, output_file_path)