from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AnswerBase(BaseModel):
    answer: str = Field(description="Ответ")
    sec_value: int = Field(description="Уровень безопасности")


class AnswerCreate(BaseModel):
    answer: str = Field(description="Ответ")
    sec_value: int = Field(description="Уровень безопасности", ge=1, le=5)


class AnswerRead(AnswerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AnswerReadList(AnswerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AnswerUpdate(BaseModel):
    answer: Optional[str] = None
    sec_value: Optional[int] = None
