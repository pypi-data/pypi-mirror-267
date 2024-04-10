from sqlalchemy.orm import Session
from connect import engine
from models import Base, TA, Course, Instructor, Section, Schedule, Assignment

import json



with open("output_files/ta_schedule.json", 'r') as file:
    ta_sched = json.load(file)

with open("output_files/courses.json", 'r') as file:
    courses = json.load(file)

# TODO - fix this part
# with open("output_files/faculty.json", 'r') as file:
#     instructors = json.load(file)

with open("output_files/unique_sections.json", 'r') as file:
    sections = json.load(file)

with open("output_files/schedule.json", 'r') as file:
    schedules = json.load(file)

with open("assignment_output_files/ta_assignments.json", 'r') as file:
    assignments = json.load(file)

session = Session(bind=engine)

ta_list = []
course_list = []
section_list = []
schedule_list = []
assignment_list = []

for ta in ta_sched:
    obj = TA(uga_id=int(ta["UGAID"]), fname=ta["fname"], lname=ta["lname"], uga_email=ta["email"])
    ta_list.append(obj)

for course in courses:
    obj = Course(course_no = course["course_no"], course_name = course["course_name"], credit_hours = course["credit_hours"])
    course_list.append(obj)

for section in sections:
    obj = Section(crn = section["crn"], course_no=section["course_no"], instructor_id = section["ins_fname"] + section["ins_lname"], lab = section["lab"], enrolled = int(section["enrolled"]), capacity = int(section["capacity"]))
    section_list.append(obj)

for schedule in schedules:
    obj = Schedule(schedule_id = schedule["schedule_id"], crn = schedule["crn"], slot = schedule["slot"])
    schedule_list.append(obj)

for index, assignment in enumerate(assignments):
    # obj = Assignment(assignment_id = index + 1, ta_id = assignment["ta_id"], section_id = assignment["crn"], ta_hours = assignment["ta_hours"])
    obj = Assignment(assignment_id = index + 1, uga_id = assignment["uga_id"], crn = assignment["crn"], ta_hours = "17.78")
    assignment_list.append(obj)

session.add_all(ta_list)
session.add_all(course_list)
session.add_all(section_list)
session.add_all(schedule_list)
session.add_all(assignment_list)

session.commit()
