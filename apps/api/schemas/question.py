from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from .source import SourceRead
from .answer import AnswerRead


class QuestionBase(BaseModel):
    question: str = Field(description="Вопрос")


class QuestionCreate(BaseModel):
    question: str = Field(description="Вопрос")


class QuestionRead(QuestionBase):
    id: int
    source: Optional[SourceRead] = Field(description="Источник")
    answers: List[AnswerRead] = Field(description="Ответы")
    model_config = ConfigDict(from_attributes=True)


class QuestionReadList(QuestionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    source_id: Optional[int] = None
