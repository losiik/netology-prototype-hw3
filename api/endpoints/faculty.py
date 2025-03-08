from fastapi import APIRouter, Security
from fastapi.exceptions import HTTPException

from fastapi_jwt import JwtAuthorizationCredentials

from api.jwt import access_security, is_token_blacklisted


from services.faculty_service import FacultyService
from schemas import Faculty

faculty_service = FacultyService()

faculty_router = APIRouter(prefix='/faculty')
faculty_router.tags = ["Faculty"]


@faculty_router.get("/", response_model=Faculty)
async def get_faculty(
        faculty_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    faculty = await faculty_service.get_faculty(faculty_id=faculty_id)
    return faculty


@faculty_router.delete("/", response_model=Faculty)
async def delete_faculty(
        faculty_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    faculty = await faculty_service.delete_faculty(faculty_id=faculty_id)
    return faculty


@faculty_router.put("/", response_model=Faculty)
async def add_faculty(
        faculty: Faculty,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    faculty = await faculty_service.add_faculty(faculty=faculty)
    return faculty


@faculty_router.patch("/", response_model=Faculty)
async def update_faculty(
        faculty: Faculty,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    faculty = await faculty_service.update_faculty(faculty=faculty)
    return faculty
