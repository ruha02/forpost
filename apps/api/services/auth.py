from fastapi_users.authentication import JWTStrategy
from core.settings import get_settings
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi import Depends
from core.database import get_db
from fastapi_users.db import SQLAlchemyUserDatabase
from models import User
from fastapi_users import FastAPIUsers
from passlib.context import CryptContext
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
    )


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()
bearer_transport = BearerTransport(tokenUrl="auth/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


def get_user_db(session=Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key


def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


users_api = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
