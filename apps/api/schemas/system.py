from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .user import UserRead


class SystemBase(BaseModel):
    create_at: datetime = Field(description="Дата")
    name: str = Field(description="Название")
    description: Optional[str] = Field(description="Описание", nullable=True)
    repo: Optional[str] = Field(description="Репозиторий", nullable=True)


class SystemCreate(BaseModel):
    name: str = Field(description="Название")
    description: Optional[str] = Field(description="Описание", nullable=True)
    repo: Optional[str] = Field(description="Репозиторий", nullable=True)


class SystemRead(SystemBase):
    id: int
    owner: Optional[UserRead] = Field(description="Пользователь")
    chat: Optional[dict] = Field(description="Чат")
    model_config = ConfigDict(from_attributes=True)


class SystemReadList(SystemBase):
    id: int
    owner: Optional[UserRead] = Field(description="Пользователь")
    model_config = ConfigDict(from_attributes=True)


class SystemUpdate(BaseModel):
    create_at: Optional[datetime] = None
    name: Optional[str] = None
    description: Optional[str] = None
    repo: Optional[str] = None
    owner_id: Optional[int] = None


class Message(BaseModel):
    date: datetime
    role: str
    text: str
