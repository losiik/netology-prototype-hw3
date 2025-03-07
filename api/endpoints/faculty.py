from fastapi import APIRouter

from services.faculty_service import FacultyService
from schemas import Faculty

faculty_service = FacultyService()

faculty_router = APIRouter(prefix='/faculty')
faculty_router.tags = ["Faculty"]


@faculty_router.get("/", response_model=Faculty)
async def get_faculty(faculty_id: int):
    faculty = await faculty_service.get_faculty(faculty_id=faculty_id)
    return faculty


@faculty_router.delete("/", response_model=Faculty)
async def delete_faculty(faculty_id: int):
    faculty = await faculty_service.delete_faculty(faculty_id=faculty_id)
    return faculty


@faculty_router.put("/", response_model=Faculty)
async def add_faculty(faculty: Faculty):
    faculty = await faculty_service.add_faculty(faculty=faculty)
    return faculty


@faculty_router.patch("/", response_model=Faculty)
async def update_faculty(faculty: Faculty):
    faculty = await faculty_service.update_faculty(faculty=faculty)
    return faculty
