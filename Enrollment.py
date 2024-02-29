from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint, Identity, ForeignKey
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from typing import List


class Enrollment(Base):
    __tablename__ = "enrollments"
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10),
                                                            primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer,
                                                primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), CheckConstraint("semester IN('Fall','Spring','Winter','Summer I','Summer II')", name="semester_check"), 
                                          primary_key=True)
    
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer,
                                                primary_key=True)

    section: Mapped["Section"] = relationship(back_populates="students")

    studentID: Mapped[int] = mapped_column('student_id', Integer, 
                                           ForeignKey("students.student_id"), 
                                           primary_key=True)
    student: Mapped["Student"] = relationship(back_populates="sections")

    __table_args__= (UniqueConstraint("department_abbreviation", "course_number", "section_year", "semester", "student_id", name="enrollments_uk_01"),
                    ForeignKeyConstraint([departmentAbbreviation, courseNumber, sectionNumber, sectionYear, semester], 
                                         ["sections.department_abbreviation", "sections.course_number", "sections.section_number", "sections.section_year", "sections.semester"]),)
    
    def __init__(self, section, student):
        self.section = section
        self.student = student
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionNumber = section.sectionNumber
        self.sectionYear = section.sectionYear
        self.semester = section.semester
        self.studentID = student.studentID

    def __str__(self):
        return f"Student section - student: {self.studentID} section: {self.section}"

