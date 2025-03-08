from fastapi import APIRouter

from api.endpoints.academic_performance import academic_performance_router
from api.endpoints.course import course_router
from api.endpoints.faculty import faculty_router
from api.endpoints.student import student_router
from api.endpoints.auth import auth_router


api_router = APIRouter()
api_router.include_router(academic_performance_router)
api_router.include_router(course_router)
api_router.include_router(faculty_router)
api_router.include_router(student_router)
api_router.include_router(auth_router)
