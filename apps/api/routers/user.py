from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate, UserRead, UserReadList, UserUpdate
from services import (
    get_user,
    get_users,
    create_user,
    count_user,
    update_user,
    delete_user
)


router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=UserRead)
def route_create(
    create: UserCreate,
    db: Session = Depends(get_db),
) -> UserRead:
    return create_user(db=db, create=create)


@router.get("/", response_model=list[UserReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
) -> list[UserReadList]:
    return get_users(db=db, offset=pagination.offset, limit=pagination.limit)


@router.get("/{id}", response_model=UserRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
) -> UserRead:
    result = get_user(db=db, id=id)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
) -> int:
    return  count_user(db=db)


@router.patch("/{id}", response_model=UserRead)
def route_update(
    id: int,
    update: UserUpdate,
    db: Session = Depends(get_db),
) -> UserRead:
    return update_user(db=db, id=id, update=update)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
) -> SuccessResult:
    return delete_user(db=db, id=id)