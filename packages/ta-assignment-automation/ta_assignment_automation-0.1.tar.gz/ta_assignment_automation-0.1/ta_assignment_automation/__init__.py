# UTIL imports
from .src.utils.convertCSVtoJSON import convertInputFilesToJSON
from .src.utils.csvToDict import read_csv_to_dict
from .src.utils.dictionaryToJsonFile import write_dict_to_json
from .src.utils.filterDigits import filter_digits
from .src.utils.load_conflict_matrix import getConflictMatFromTxt
from .src.utils.saveMatirxToTxtFile import saveMatToTxt
from .src.utils.setCurrDirToBase import setCurrDirToBase
from .src.utils.create_required_folders import create_required_folders

# CONFIG IMPORTS
from .src.config.capacity_cap import getCapacityCap
from .src.config.daysMapping import getDaysMap
# from .src.config.db_config import db_url
from .src.config.edgeWeights import getEdgeWeights
from .src.config.getPseudoLabs import getPseudoLabs
from .src.config.lab_ta_requirements import getLabTAReq
from .src.config.timeSlotMapping import getTimeSlotMapping


from .src.algorithms.hungarian import hungarian

# from .src.db_access import(
#     connect,
#     create_tables,
#     insert_data,
#     models
# )

from .src.scripts.combined_view import combine_course_schedules
from .src.scripts.compute_conflict_matrix import computeConflictMatrix
from .src.scripts.create_conflict_breakdown_skeleton import createConflictBreakdownSkeleton
from .src.scripts.create_final_sections import create_final_sections
from .src.scripts.duplicateTAs import duplicateTAs
from .src.scripts.getCoursesTakenFromCrn import getCoursesTakenFromCRN
from .src.scripts.getTimeSlotsFromCRN import getTimeSlotsFromCRN
from .src.scripts.incremental_TA_duplication import incremental_TA_duplication
from .src.scripts.parse_courses import parseCourses
from .src.scripts.parse_instructor_pref import parseInstructorPref
from .src.scripts.parse_schedule import parseSchedule
from .src.scripts.parse_sections import parseSections
from .src.scripts.parse_ta_data import parseTAData
from .src.scripts.show_hungarian_assignments import showAssignments
from .src.scripts.splitTAHours import splitTAhours
# from .src.scripts.process_labs import 
