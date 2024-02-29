from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List                 # Use this for the list of courses offered by the department


class Department(Base):
    """This is the guts of the department class that needs to be defined
    regardless whether we introspect or not."""
    __tablename__ = "departments"  # Give SQLAlchemy th name of the table.
    abbreviation: Mapped[str] = mapped_column('abbreviation', String(10),
                                            nullable=False, primary_key=True)
    courses: Mapped[List["Course"]] = relationship(back_populates="department")
    majors: Mapped[List["Major"]] = relationship(back_populates="department")
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    chairName: Mapped[str] = mapped_column('chair_name', String(80), nullable=False)
    building: Mapped[str] = mapped_column('building', String(10), nullable=False)
    office: Mapped[int] = mapped_column('office', Integer, nullable=False)
    description: Mapped[str] = mapped_column('description', String(80), nullable=False)
    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want two separate uniqueness
    # constraints (candidate keys).
    __table_args__ = ((UniqueConstraint("abbreviation", name="departments_uk_01"), 
                    UniqueConstraint("name", name="departments_uk_02"),
                      UniqueConstraint("building", "office", name="departments_uk_03"),
                      UniqueConstraint("description", name="departments_uk_04"),
                      UniqueConstraint("chair_name", name="departments_uk_05")))

    def __init__(self, name : str, abbreviation : str, chairName : str, building : str, office : int, description : str):
        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chairName
        self.building = building 
        self.office = office 
        self.description = description


    def add_course(self, course):
        if course not in self.courses:
            self.courses.add(course)            # I believe this will update the course as well.

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return f"Department name: {self.name}, {self.abbreviation}\nChair Man: {self.chairName}, Building: {self.building}, Office: {self.office}\nDescription: {self.description}"