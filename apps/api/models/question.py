from core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(String)
    source_id = Column(Integer, ForeignKey("source.id"))
    source = relationship("Source", foreign_keys="[Question.source_id]")
    answers = relationship("Answer", back_populates="question", cascade="all, delete")
