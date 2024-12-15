from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from depends import current_active_user, current_admin_user
from fastapi import APIRouter, Depends
from schemas import UserCreate, UserRead, UserReadList, UserUpdate
from services import (
    count_user,
    create_user,
    delete_user,
    get_user,
    get_users,
    update_user,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserRead)
def route_create(
    create: UserCreate,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> UserRead:
    user = create_user(db=db, create=create)
    print(f"{'*'*20}{user}")
    return user


@router.get("/", response_model=list[UserReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
    user: UserRead = Depends(current_admin_user),
) -> list[UserReadList]:
    return get_users(db=db, offset=pagination.offset, limit=pagination.limit)


@router.get("/{id}", response_model=UserRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> UserRead:
    result = get_user(db=db, id=id)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> int:
    return count_user(db=db)


@router.patch("/{id}", response_model=UserRead)
def route_update(
    id: int,
    update: UserUpdate,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> UserRead:
    return update_user(db=db, id=id, update=update)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_admin_user),
) -> SuccessResult:
    return delete_user(db=db, id=id)


@router.get("/me/", response_model=UserRead)
def route_get_me(
    current_user: UserRead = Depends(current_active_user),
) -> UserRead:
    return current_user
