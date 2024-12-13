from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .answer import AnswerRead
from .source import SourceRead


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
    answers: List[AnswerRead] = Field(description="Ответы")
    source: Optional[SourceRead] = Field(description="Источник")
    model_config = ConfigDict(from_attributes=True)


class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    source_id: Optional[int] = None
