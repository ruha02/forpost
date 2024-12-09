from core.database import Base
from sqlalchemy import Column, Integer
from sqlalchemy import String


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    password = Column(String)
    role = Column(String)
    