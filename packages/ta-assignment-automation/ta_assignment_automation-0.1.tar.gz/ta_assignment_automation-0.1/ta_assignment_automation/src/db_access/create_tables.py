from models import Base, Course, TA, Instructor, Schedule, Section, Assignment
from connect import engine

print("CREATING TABLES IN THE DATABASE")

Base.metadata.create_all(bind=engine)