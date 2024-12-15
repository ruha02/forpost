import os
from datetime import datetime

from core.schema import SuccessResult
from fastapi import HTTPException, status
from models import System
from requests import Session as HTTPSession
from schemas import (
    Message,
    SystemCreate,
    SystemRead,
    SystemReadList,
    SystemUpdate,
    UserRead,
)
from sqlalchemy.orm import Session


def get_system(db: Session, id: int, user: UserRead) -> SystemRead:
    try:
        if user.is_superuser:
            result = db.query(System).filter(System.id == id).first()
        else:
            result = (
                db.query(System)
                .filter(System.id == id, System.owner_id == user.id)
                .first()
            )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_systems(
    db: Session,
    user: UserRead,
    offset: int = 0,
    limit: int | None = None,
) -> list[SystemReadList]:
    try:
        if user.is_superuser:
            result = db.query(System).offset(offset).limit(limit).all()
        else:
            result = (
                db.query(System)
                .filter(System.owner_id == user.id)
                .offset(offset)
                .limit(limit)
                .all()
            )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def create_system(db: Session, create: SystemCreate, user: UserRead) -> SystemRead:
    try:
        db_instance = System(**create.model_dump())
        db_instance.owner_id = user.id
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def count_system(db: Session, user: UserRead) -> int:
    try:
        if user.is_superuser:
            result = db.query(System.id).count()
        else:
            result = db.query(System).filter(System.owner_id == user.id).count()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result


def update_system(
    db: Session, id: int, update: SystemUpdate, user: UserRead
) -> SystemRead:
    try:
        db_instance: System = get_system(db=db, id=id, user=user)
        if not db_instance:
            raise HTTPException(status_code=404, detail="Record not found")
        update_data = update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_instance, key, value)
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def find_system(db: Session, default: dict, user: UserRead) -> SystemRead | None:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(System, key) == default.get(key, None))
        if not user.is_superuser:
            statements.append(System.owner_id == user.id)
        result = db.query(System).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.first()


def find_systems(db: Session, default: dict, user: UserRead) -> list[SystemReadList]:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(System, key) == default.get(key, None))
        if not user.is_superuser:
            statements.append(System.owner_id == user.id)
        result = db.query(System).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.all()


def delete_system(db: Session, id: int, user: UserRead) -> SuccessResult:
    try:
        db_instance = get_system(db=db, id=id, user=user)
        if not db_instance:
            raise HTTPException(status_code=404, detail="Record not found")
        db.delete(db_instance)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return SuccessResult(success=True)


def get_system_messages(db: Session, id: int, user: UserRead) -> list[Message]:
    try:
        result = get_system(db=db, id=id, user=user)
        if not result:
            raise HTTPException(status_code=404, detail="Record not found")
        messages_list = result.chat.get("messages", [])
        result = [Message(**message) for message in messages_list]
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def send_system_message(
    db: Session, id: int, text: str, user: UserRead
) -> SuccessResult:
    result = get_system(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="Record not found")
    messages_list = result.chat.get("messages", [])
    messages_list.append(
        {
            "role": "user",
            "text": text,
            "date": datetime.now().isoformat(),
        }
    )
    # Кирилл тут надо будет заменить на запрос к сервису
    try:
        s = HTTPSession()
        r = s.post(
            "http://127.0.0.1:8000/api/v1/chat/send_message/",
            json={"id": id, "message": text},
        )
        response = r.json()
        messages_list.append(
            {
                "role": "system",
                "text": response["text"],
                "date": datetime.now().isoformat(),
            }
        )
    except Exception as err:
        print(f"Error: {err=}")
        messages_list.append(
            {
                "role": "system",
                "text": "Я устал... и не буду работать...",
                "date": datetime.now().isoformat(),
            }
        )
    print("Before update:", result.chat)
    result.chat = {"messages": messages_list}
    print("After update:", result.chat)
    db.add(result)
    db.commit()
    db.flush()
    db.refresh(result)
    result = [Message(**m) for m in messages_list]
    return result


def get_system_report(db: Session, id: int, user: UserRead) -> list[Message]:
    result = get_system(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="Record not found")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "media", str(id), "report.pdf")
    if os.path.exists(file_path):
        return f"http://localhost/files/{id}/report.pdf"
    return None
