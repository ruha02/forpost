from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    name: str = Field(description="Имя")
    password: str = Field(description="Пароль")
    role: str = Field(description="Роль")
    

class UserCreate(BaseModel):
    name: str = Field(description="Имя")
password: str = Field(description="Пароль")
role: str = Field(description="Роль")


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserReadList(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    