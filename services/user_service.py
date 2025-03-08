from hashlib import sha256

from fastapi_sqlalchemy import db
from fastapi.exceptions import HTTPException

from services.db_operations import DBOperations
from models import User

from schemas import User as UserSchema, AuthUser
from api.jwt import access_security


class UserService(DBOperations):
    @staticmethod
    async def __user_model_to_schema(user) -> UserSchema:
        return UserSchema(id=user.id, login=user.login, password=user.password)

    @staticmethod
    def __hash_password(password: str) -> str:
        hash_object = sha256()
        hash_object.update(password.encode())
        return hash_object.hexdigest()

    async def get_user(self, user_id: int = None, login: str = None, password: str = None):
        user = None

        if user_id is not None:
            user = db.session.query(User).filter(User.id == user_id).first()
        if login is not None:
            user = db.session.query(User).filter(User.login == login).first()
        if password is not None:
            password = self.__hash_password(password=password)
            user = db.session.query(User).filter(
                User.login == login,
                User.password == password
            ).first()

        return user

    async def add_user(self, user: UserSchema) -> UserSchema:
        user_model = await self.get_user(login=user.login)
        if user_model is not None:
            raise HTTPException(status_code=400, detail="User with this login already exists")

        password = self.__hash_password(password=user.password)

        user = User(
            login=user.login,
            password=password
        )
        await self.db_write(user)
        return await self.__user_model_to_schema(user=user)

    async def registr(self, user: UserSchema) -> AuthUser:
        user = await self.add_user(user=user)
        subject = {"id": user.id}
        access_token = access_security.create_access_token(subject=subject)
        return AuthUser(id=user.id, login=user.login, access_token=access_token)

    async def auth_user(self, user: UserSchema) -> AuthUser:
        user = await self.get_user(login=user.login, password=user.password)

        if user is None:
            raise HTTPException(status_code=400, detail="Incorrect login or password")

        subject = {"id": user.id}
        access_token = access_security.create_access_token(subject=subject)
        return AuthUser(id=user.id, login=user.login, access_token=access_token)
