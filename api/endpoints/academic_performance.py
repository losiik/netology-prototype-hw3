from fastapi import APIRouter, Security
from fastapi.exceptions import HTTPException
from fastapi_jwt import JwtAuthorizationCredentials

from api.jwt import access_security, is_token_blacklisted

from schemas import AcademicPerformance
from services.academic_performance_service import AcademicPerformanceService

academic_performance_service = AcademicPerformanceService()

academic_performance_router = APIRouter(prefix='/academic_performance')
academic_performance_router.tags = ["AcademicPerformance"]


@academic_performance_router.delete("/", response_model=AcademicPerformance)
async def get_academic_performance(
        academic_performance_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    academic_performance = await academic_performance_service.get_academic_performance(
        academic_performance_id=academic_performance_id
    )
    return academic_performance


@academic_performance_router.delete("/", response_model=AcademicPerformance)
async def delete_academic_performance(
        academic_performance_id: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    academic_performance = await academic_performance_service.delete_academic_performance(
        academic_performance_id=academic_performance_id
    )
    return academic_performance


@academic_performance_router.put("/", response_model=AcademicPerformance)
async def add_academic_performance(
        academic_performance: AcademicPerformance,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    academic_performance = await academic_performance_service.add_academic_performance(
        academic_performance=academic_performance
    )
    return academic_performance


@academic_performance_router.patch("/", response_model=AcademicPerformance)
async def update_academic_performance(
        academic_performance: AcademicPerformance,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")

    academic_performance = await academic_performance_service.update_academic_performance(
        academic_performance=academic_performance
    )
    return academic_performance
