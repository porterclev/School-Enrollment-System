from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from Course import Course
from Enrollment import Enrollment
from typing import List

class Section(Base):
    __tablename__ = "sections"
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10),
                                                            primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                primary_key=True)
    course: Mapped["Course"] = relationship(back_populates="sections")
    students: Mapped[List["Enrollment"]] = relationship(back_populates="section",
                                                        cascade="all, save-update, delete-orphan")
    sectionYear: Mapped[int] = mapped_column('section_year', Integer,
                                                nullable=False, primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer,
                                                nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), CheckConstraint("semester IN('Fall','Spring','Winter','Summer I','Summer II')", name="semester_check"),
                                            nullable=False, primary_key=True)
    room: Mapped[int] = mapped_column('room', Integer,
                                        nullable=False)
    building: Mapped[str] = mapped_column('building', String(6), CheckConstraint("building IN('VEC','ECS','EN2','EN3','EN4','ET','SSPA')", name="building_check"),
                                            nullable=False)
    schedule: Mapped[str] = mapped_column('schedule', String(6), CheckConstraint("schedule IN('MW','TuTh','MWF','F','S')", name="schedule_check"),
                                            nullable=False)
    startTime: Mapped[str] = mapped_column('start_time', Integer, nullable=False)
    instructor: Mapped[str] = mapped_column('instructor', String(80),
                                            nullable=False)

    __table_args__ = (UniqueConstraint("section_year", "semester", "schedule", "start_time", "building", "room",
                                        name="sections_uk_01"),
                        UniqueConstraint("section_year", "semester", "schedule", "start_time", "instructor",
                                        name="sections_uk_02"),
                        ForeignKeyConstraint([departmentAbbreviation, courseNumber],
                                            [Course.departmentAbbreviation, Course.courseNumber]))
    
    def __init__(self, course: Course, sectionYear: int, sectionNumber: int, semester: str, room: int, building: str, schedule: str, startTime: int, instructor: str):
        self.set_course(course)
        self.sectionYear = sectionYear
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.room = room 
        self.building = building 
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor


    def add_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                return              
        student_section = Enrollment(self, student)

    def remove_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                self.students.remove(next_student)
                return True
        return False

    def set_course(self, course: Course):
        """
        Accept a new department withoug checking for any uniqueness.
        I'm going to assume that either a) the caller checked that first
        and/or b) the database will raise its own exception.
        :param department:  The new department for the course.
        :return:            None
        """
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber

    def __str__(self):
        return f"Department abbrev: {self.departmentAbbreviation} number: {self.courseNumber} year: {self.sectionYear} semester: {self.semester} section: {self.sectionNumber} building: {self.building} room: {self.room} schedule: {self.schedule} time: {self.startTime} instructor: {self.instructor}"