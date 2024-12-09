from core.database import Base
from sqlalchemy import Column, Integer
from sqlalchemy import String, Integer


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)

    answer = Column(String)
    sec_value = Column(Integer)
    