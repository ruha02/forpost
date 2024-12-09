from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import SourceCreate, SourceRead, SourceReadList, SourceUpdate
from services import (
    get_source,
    get_sources,
    create_source,
    count_source,
    update_source,
    delete_source
)


router = APIRouter(prefix="/source", tags=["Source"])

@router.post("/", response_model=SourceRead)
def route_create(
    create: SourceCreate,
    db: Session = Depends(get_db),
) -> SourceRead:
    return create_source(db=db, create=create)


@router.get("/", response_model=list[SourceReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
) -> list[SourceReadList]:
    return get_sources(db=db, offset=pagination.offset, limit=pagination.limit)


@router.get("/{id}", response_model=SourceRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
) -> SourceRead:
    result = get_source(db=db, id=id)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
) -> int:
    return  count_source(db=db)


@router.patch("/{id}", response_model=SourceRead)
def route_update(
    id: int,
    update: SourceUpdate,
    db: Session = Depends(get_db),
) -> SourceRead:
    return update_source(db=db, id=id, update=update)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
) -> SuccessResult:
    return delete_source(db=db, id=id)