from fastapi import APIRouter, Security, UploadFile, File
from fastapi.exceptions import HTTPException

from fastapi_jwt import JwtAuthorizationCredentials

from api.jwt import access_security, is_token_blacklisted


from services.faculty_service import FacultyService
from schemas import Faculty

faculty_service = FacultyService()

csv_router = APIRouter(prefix='/csv')
csv_router.tags = ["Csv"]


@csv_router.post("/upload/", response_model=bool)
async def upload(
        document: UploadFile = File(),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")


@csv_router.post("/delete/", response_model=bool)
async def delete(
        document: UploadFile = File(),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    if is_token_blacklisted(token=credentials.jti):
        raise HTTPException(status_code=400, detail="User not authorized")
