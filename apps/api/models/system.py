from core.database import Base
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class System(Base):
    __tablename__ = "system"

    id = Column(Integer, primary_key=True, index=True)

    create_at = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    name = Column(String)
    description = Column(String, nullable=True)
    chat = Column(JSON, nullable=True)

    repo = Column(String, nullable=True)
    report = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", foreign_keys="[System.owner_id]")
