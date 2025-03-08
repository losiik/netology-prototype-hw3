from typing import List

from fastapi import APIRouter, Security
from fastapi.exceptions import HTTPException
from fastapi_jwt import JwtAuthorizationCredentials

from api.jwt import access_security, is_token_blacklisted


from schemas import Student
from services.student_service import StudentService

student_service = StudentService()

student_router = APIRouter(prefix='/student')
student_router.tags = ["Student"]


@student_router.get("/list/", response_model=List[Student] | None)
async def students_list(
        faculty_name: str = None,
        course_name: str = None,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    students = await student_service.get_students_list(
        faculty_name=faculty_name,
        course_name=course_name
    )

    return students


@student_router.get("/avg_mark/", response_model=float)
async def avg_mark(
        faculty_name: str,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    mark = await student_service.get_average_mark_by_faculty(faculty_name=faculty_name)
    return mark


@student_router.get("/", response_model=Student)
async def get_student(
        student_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    student = await student_service.get_student(student_id=student_id)
    return student


@student_router.delete("/", response_model=Student)
async def delete_student(
        student_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    student = await student_service.delete_student(student_id=student_id)
    return student


@student_router.put("/", response_model=Student)
async def add_student(
        student: Student,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    student = await student_service.add_student(student=student)
    return student


@student_router.patch("/", response_model=Student)
async def update_student(
        student: Student,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    student = await student_service.update_student(student=student)
    return student
