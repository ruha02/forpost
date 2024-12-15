from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from filters import QuestionFilter
from schemas import QuestionCreate, QuestionRead, QuestionReadList, QuestionUpdate
from services import (
    count_question,
    create_question,
    delete_question,
    get_question,
    get_questions,
    update_question,
)
from sqlalchemy.orm import Session

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
    filter: QuestionFilter = FilterDepends(QuestionFilter),
) -> list[QuestionReadList]:
    return get_questions(
        db=db, offset=pagination.offset, limit=pagination.limit, filter=filter
    )


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
    filter: QuestionFilter = FilterDepends(QuestionFilter),
) -> int:
    return count_question(db=db, filter=filter)


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
