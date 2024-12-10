from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserBase(BaseUser):
    pass


class UserCreate(BaseUserCreate):
    pass


class UserRead(UserBase):
    pass


class UserReadList(UserBase):
    pass


class UserUpdate(BaseUserUpdate):
    pass
