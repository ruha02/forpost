from core.database import get_db
from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from depends import current_active_user
from fastapi import APIRouter, Depends
from schemas import (
    Message,
    SystemCreate,
    SystemRead,
    SystemReadList,
    SystemUpdate,
    UserRead,
)
from services import (
    count_system,
    create_system,
    delete_system,
    get_system,
    get_system_messages,
    get_system_report,
    get_systems,
    send_system_message,
    update_system,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/system", tags=["System"])


@router.post("/", response_model=SystemRead)
def route_create(
    create: SystemCreate,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> SystemRead:
    return create_system(db=db, create=create, user=user)


@router.get("/", response_model=list[SystemReadList])
def route_get_all(
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination),
    user: UserRead = Depends(current_active_user),
) -> list[SystemReadList]:
    return get_systems(
        db=db, offset=pagination.offset, limit=pagination.limit, user=user
    )


@router.get("/{id}", response_model=SystemRead)
def route_get_one(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> SystemRead:
    result = get_system(db=db, id=id, user=user)
    if result is None:
        raise NotFound()
    return result


@router.get("/count/", response_model=int)
def route_count(
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> int:
    return count_system(db=db, user=user)


@router.patch("/{id}", response_model=SystemRead)
def route_update(
    id: int,
    update: SystemUpdate,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> SystemRead:
    return update_system(db=db, id=id, update=update, user=user)


@router.delete("/{id}", response_model=SuccessResult)
def route_delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> SuccessResult:
    return delete_system(db=db, id=id, user=user)


@router.get("/{id}/messages/", response_model=list[Message])
def route_get_messages(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> list[Message]:
    return get_system_messages(db=db, id=id, user=user)


@router.post("/{id}/send_message/", response_model=list[Message])
def route_send_message(
    id: int,
    text: str,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> list[Message]:
    print(id, text)
    return send_system_message(db=db, id=id, text=text, user=user)


@router.get("/{id}/report/", response_model=str | None)
def route_get_report(
    id: int,
    db: Session = Depends(get_db),
    user: UserRead = Depends(current_active_user),
) -> str | None:
    return get_system_report(db=db, id=id, user=user)
