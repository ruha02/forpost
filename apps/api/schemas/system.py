from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from .user import UserRead


class SystemBase(BaseModel):
    create_at: datetime = Field(description="Дата")
    name: str = Field(description="Название")
    description: Optional[str] = Field(description="Описание", nullable=True)
    repo: Optional[str] = Field(description="Репозиторий", nullable=True)
    report: Optional[str] = Field(description="Отчет")


class SystemCreate(BaseModel):
    create_at: datetime = Field(description="Дата")
    name: str = Field(description="Название")
    report: str = Field(description="Отчет")


class SystemRead(SystemBase):
    id: int
    owner: Optional[UserRead] = Field(description="Пользователь")
    model_config = ConfigDict(from_attributes=True)


class SystemReadList(SystemRead):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SystemUpdate(BaseModel):
    create_at: Optional[datetime] = None
    name: Optional[str] = None
    description: Optional[str] = None
    repo: Optional[str] = None
    report: Optional[str] = None
    owner_id: Optional[int] = None
