from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SourceBase(BaseModel):
    name: str = Field(description="Название")
    url: str = Field(description="Ссылка")
    

class SourceCreate(BaseModel):
    name: str = Field(description="Название")
url: str = Field(description="Ссылка")


class SourceRead(SourceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SourceReadList(SourceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    