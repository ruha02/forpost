from core.database import Base
from sqlalchemy import Column, Integer
from sqlalchemy import DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(DateTime)
    name = Column(String)
    description = Column(String, nullable=True)
    status = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", foreign_keys="[Task.user_id]")
    