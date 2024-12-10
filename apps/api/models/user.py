from core.database import Base
from sqlalchemy import Column, Integer
from fastapi_users.db import SQLAlchemyBaseUserTable


class User(SQLAlchemyBaseUserTable, Base):
    id = Column(Integer, primary_key=True, index=True)
    pass
