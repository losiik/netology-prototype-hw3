from typing import List
from fastapi import APIRouter

from schemas import Student, Course
from student_service import StudentService

student_service = StudentService()

student_router = APIRouter(prefix='/student')
student_router.tags = ["Student"]


@student_router.get("/students_list/", response_model=List[Student] | None)
async def students_list(faculty_name: str = None, course_name: str = None):
    students = await student_service.get_students_list(
        faculty_name=faculty_name,
        course_name=course_name
    )

    return students


@student_router.get("/course_list/", response_model=List[Course])
async def course_list():
    courses = await student_service.get_courses()
    return courses


@student_router.get("/avg_mark/", response_model=float)
async def avg_mark(faculty_name: str):
    mark = await student_service.get_average_mark_by_faculty(faculty_name=faculty_name)
    return mark
