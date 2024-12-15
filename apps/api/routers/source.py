from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from depends import current_active_user, current_admin_user
from fastapi import APIRouter, Depends
from schemas import SourceCreate, SourceRead, SourceReadList, SourceUpdate, UserRead
from services import (
    count_source,
    create_source,
    delete_source,
    get_source,
    get_sources,
    update_source,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/source", tags=["Source"])


@router.post("/", response_model=SourceRead)
def route_create(
    create: SourceCreate,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> SourceRead:
    return create_source(db=db, create=create)


@router.get("/", response_model=list[SourceReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
    user: UserRead = Depends(current_active_user),
) -> list[SourceReadList]:
    return get_sources(db=db, offset=pagination.offset, limit=pagination.limit)


@router.get("/{id}", response_model=SourceRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> SourceRead:
    result = get_source(db=db, id=id)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> int:
    return count_source(db=db)


@router.patch("/{id}", response_model=SourceRead)
def route_update(
    id: int,
    update: SourceUpdate,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> SourceRead:
    return update_source(db=db, id=id, update=update)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> SuccessResult:
    return delete_source(db=db, id=id)
