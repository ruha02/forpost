from core.database import Base
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class System(Base):
    __tablename__ = "system"

    id = Column(Integer, primary_key=True, index=True)

    create_at = Column(DateTime)
    name = Column(String)
    description = Column(String, nullable=True)
    chat = Column(JSON, nullable=True)

    repo = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", foreign_keys="[System.owner_id]")
