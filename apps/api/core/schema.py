from pydantic import BaseModel


class SuccessResult(BaseModel):
    success: bool


class Pagination(BaseModel):
    offset: int = 0
    limit: int | None = None
