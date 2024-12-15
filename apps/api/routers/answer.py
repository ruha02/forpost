from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from fastapi import APIRouter, Depends
from schemas import AnswerCreate, AnswerRead, AnswerReadList, AnswerUpdate
from services import (
    count_answer,
    create_answer,
    delete_answer,
    get_answer,
    get_answers,
    update_answer,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/answer", tags=["Answer"])


@router.post("/", response_model=AnswerRead)
def route_create(
    create: AnswerCreate,
    db: Session = Depends(get_db),
) -> AnswerRead:
    return create_answer(db=db, create=create)


@router.get("/", response_model=list[AnswerReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
) -> list[AnswerReadList]:
    return get_answers(db=db, offset=pagination.offset, limit=pagination.limit)


@router.get("/{id}", response_model=AnswerRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
) -> AnswerRead:
    result = get_answer(db=db, id=id)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
) -> int:
    return count_answer(db=db)


@router.patch("/{id}", response_model=AnswerRead)
def route_update(
    id: int,
    update: AnswerUpdate,
    db: Session = Depends(get_db),
) -> AnswerRead:
    return update_answer(db=db, id=id, update=update)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
) -> SuccessResult:
    return delete_answer(db=db, id=id)
