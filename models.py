from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class AcademicPerformance(Base):
    __tablename__ = "academic_performance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id', ondelete='CASCADE'))
    faculty_id = Column(Integer, ForeignKey('faculty.id', ondelete='CASCADE'))
    course_id = Column(Integer, ForeignKey('course.id', ondelete='CASCADE'))
    mark = Column(Integer, nullable=False)


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, autoincrement=True)
    faculty_name = Column(String, nullable=False, unique=True)


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String, nullable=False, unique=True)
