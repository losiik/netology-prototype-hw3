from typing import List

from fastapi import APIRouter, Security
from fastapi.exceptions import HTTPException
from fastapi_jwt import JwtAuthorizationCredentials

from api.jwt import access_security, is_token_blacklisted


from schemas import Course
from services.course_service import CourseService

course_service = CourseService()

course_router = APIRouter(prefix='/course')
course_router.tags = ["Course"]


@course_router.get("/list/", response_model=List[Course])
async def course_list(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    courses = await course_service.get_courses()
    return courses


@course_router.get("/", response_model=Course)
async def get_course(
        course_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    courses = await course_service.get_course(course_id=course_id)
    return courses


@course_router.delete("/", response_model=Course)
async def delete_course(
        course_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    courses = await course_service.delete_course(course_id=course_id)
    return courses


@course_router.put("/", response_model=Course)
async def add_course(
        course: Course,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    course = await course_service.add_course(course=course)
    return course


@course_router.patch("/", response_model=Course)
async def update_course(
        course: Course,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    course = await course_service.update_course(course=course)
    return course
