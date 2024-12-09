from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import QuestionCreate, QuestionRead, QuestionReadList, QuestionUpdate
from services import (
    get_question,
    get_questions,
    create_question,
    count_question,
    update_question,
    delete_question
)


router = APIRouter(prefix="/question", tags=["Question"])

@router.post("/", response_model=QuestionRead)
def route_create(
    create: QuestionCreate,
    db: Session = Depends(get_db),
) -> QuestionRead:
    return create_question(db=db, create=create)


@router.get("/", response_model=list[QuestionReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
) -> list[QuestionReadList]:
    return get_questions(db=db, offset=pagination.offset, limit=pagination.limit)


@router.get("/{id}", response_model=QuestionRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
) -> QuestionRead:
    result = get_question(db=db, id=id)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
) -> int:
    return  count_question(db=db)


@router.patch("/{id}", response_model=QuestionRead)
def route_update(
    id: int,
    update: QuestionUpdate,
    db: Session = Depends(get_db),
) -> QuestionRead:
    return update_question(db=db, id=id, update=update)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
) -> SuccessResult:
    return delete_question(db=db, id=id)