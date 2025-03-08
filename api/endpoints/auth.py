from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials

from api.jwt import access_security, blacklist

from schemas import User, AuthUser
from services.user_service import UserService

user_service = UserService()

auth_router = APIRouter(prefix='/auth')
auth_router.tags = ["Auth"]


@auth_router.put("/", response_model=AuthUser)
async def registr(user: User):
    user = await user_service.registr(user=user)
    return user


@auth_router.post("/", response_model=AuthUser)
async def auth(user: User):
    user = await user_service.auth_user(user=user)
    return user


@auth_router.post("/logout/", response_model=dict[str, str])
async def end_session(credentials: JwtAuthorizationCredentials = Security(access_security)):
    blacklist.add(credentials.jti)
    return {"msg": "Successfully logged out"}
