from typing import List
from fastapi import APIRouter

from schemas import Student
from services.student_service import StudentService

student_service = StudentService()

student_router = APIRouter(prefix='/student')
student_router.tags = ["Student"]


@student_router.get("/list/", response_model=List[Student] | None)
async def students_list(faculty_name: str = None, course_name: str = None):
    students = await student_service.get_students_list(
        faculty_name=faculty_name,
        course_name=course_name
    )

    return students


@student_router.get("/avg_mark/", response_model=float)
async def avg_mark(faculty_name: str):
    mark = await student_service.get_average_mark_by_faculty(faculty_name=faculty_name)
    return mark


@student_router.get("/", response_model=Student)
async def get_student(student_id: int):
    student = await student_service.get_student(student_id=student_id)
    return student


@student_router.delete("/", response_model=Student)
async def delete_student(student_id: int):
    student = await student_service.delete_student(student_id=student_id)
    return student


@student_router.put("/", response_model=Student)
async def add_student(student: Student):
    student = await student_service.add_student(student=student)
    return student


@student_router.patch("/", response_model=Student)
async def update_student(student: Student):
    student = await student_service.update_student(student=student)
    return student
