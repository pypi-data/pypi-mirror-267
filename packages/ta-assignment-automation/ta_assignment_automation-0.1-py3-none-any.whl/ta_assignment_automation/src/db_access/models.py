from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class Course(Base):
    __tablename__ = "courses"

    course_no:Mapped[str] = mapped_column(primary_key=True)
    course_name:Mapped[str] = mapped_column(nullable=False)
    credit_hours:Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"<Course course_no = {self.course_no}>"


class TA(Base):
    __tablename__ = "tas"

    uga_id:Mapped[int] = mapped_column(primary_key=True)
    fname:Mapped[str] = mapped_column()
    lname:Mapped[str] = mapped_column()
    uga_email:Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"<TA Name = {self.fname} {self.lname}>"


class Instructor(Base):
    __tablename__ = "instructors"

    email:Mapped[str] = mapped_column(primary_key=True)
    fname:Mapped[str] = mapped_column()
    lname:Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"<Instrcutor Name = {self.fname} {self.lname}>"


class Section(Base):
    __tablename__ = "sections"

    crn:Mapped[int] = mapped_column(primary_key=True)
    course_no:Mapped[str] = mapped_column(ForeignKey('courses.course_no'))
    # instructor_id:Mapped[str] = mapped_column(ForeignKey('instructors.email'))
    instructor_id:Mapped[str] = mapped_column() # TODO - use the line above - do this after you do the instructor filling
    lab:Mapped[bool] = mapped_column()
    enrolled:Mapped[int] = mapped_column()
    capacity:Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"<Section crn={self.crn} course_no={self.course_no}>"


class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id:Mapped[int] = mapped_column(primary_key=True)
    crn:Mapped[int] = mapped_column(ForeignKey('sections.crn'))
    slot:Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"<Schedule crn={self.crn}>"


class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id:Mapped[int] = mapped_column(primary_key=True)
    uga_id:Mapped[int] = mapped_column(ForeignKey('tas.uga_id'))
    crn:Mapped[int] = mapped_column(ForeignKey('sections.crn'))
    ta_hours:Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"<Assignments ta_id={self.uga_id} section_id={self.crn}>"
