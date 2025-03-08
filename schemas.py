from typing import Optional
from pydantic import BaseModel


class Student(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Course(BaseModel):
    id: Optional[int] = None
    course_name: str


class AcademicPerformance(BaseModel):
    id: Optional[int] = None
    student_id: Optional[int] = None
    faculty_id: Optional[int] = None
    course_id: Optional[int] = None
    mark: Optional[int] = None


class Faculty(BaseModel):
    id: Optional[int] = None
    faculty_name: str


class User(BaseModel):
    id: Optional[int] = None
    login: str
    password: str


class AuthUser(BaseModel):
    id: Optional[int] = None
    login: str
    access_token: str
