from core.database import Base
from sqlalchemy import Column, Integer
from sqlalchemy import String


class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    url = Column(String)
    