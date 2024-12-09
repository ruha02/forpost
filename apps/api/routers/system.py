from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import SystemCreate, SystemRead, SystemReadList, SystemUpdate
from services import (
    get_system,
    get_systems,
    create_system,
    count_system,
    update_system,
    delete_system
)


router = APIRouter(prefix="/system", tags=["System"])

@router.post("/", response_model=SystemRead)
def route_create(
    create: SystemCreate,
    db: Session = Depends(get_db),
) -> SystemRead:
    return create_system(db=db, create=create)


@router.get("/", response_model=list[SystemReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
) -> list[SystemReadList]:
    return get_systems(db=db, offset=pagination.offset, limit=pagination.limit)


@router.get("/{id}", response_model=SystemRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
) -> SystemRead:
    result = get_system(db=db, id=id)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
) -> int:
    return  count_system(db=db)


@router.patch("/{id}", response_model=SystemRead)
def route_update(
    id: int,
    update: SystemUpdate,
    db: Session = Depends(get_db),
) -> SystemRead:
    return update_system(db=db, id=id, update=update)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
) -> SuccessResult:
    return delete_system(db=db, id=id)