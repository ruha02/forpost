from core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)

    answer = Column(String)
    sec_value = Column(Integer)

    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship(
        "Question", foreign_keys="[Answer.question_id]", back_populates="answers"
    )
