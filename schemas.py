from pydantic import BaseModel


class Student(BaseModel):
    id: int
    first_name: str
    last_name: str


class Course(BaseModel):
    id: int
    course_name: str
