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

from .question import get_questionи_by_text, get_random_question


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
    if result.chat is None:
        messages_list = []
    else:
        messages_list = result.chat.get("messages", [])
    if text != "begin":
        messages_list.append(
            {
                "role": "user",
                "text": text,
                "date": datetime.now().isoformat(),
            }
        )
    if len(messages_list) > 10:
        messages_list.append(
            {
                "role": "system",
                "text": "Мы закончили опрос и готовы предоставить вам отчет",
                "date": datetime.now().isoformat(),
            }
        )
    else:
        question = get_random_question(db=db)
        messages_list.append(
            {
                "role": "system",
                "text": f"{question.question}. Возможные варианты ответа: {", ".join([answer.answer for answer in question.answers])}",
                "date": datetime.now().isoformat(),
            }
        )
    try:
        db.query(System).filter(System.id == id).update(
            {"chat": {"messages": messages_list}}
        )
    except Exception as err:
        print(err)

    db.commit()
    db.refresh(result)
    return [Message(**m) for m in messages_list]


def get_system_report(db: Session, id: int, user: UserRead) -> str:
    result = get_system(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="Record not found")
    if result.report:
        return result.report
    report = "### Отчет по опросу\n"
    sec_level = ["Не несет", "Низкий", "Средний", "Высокий", "Очень высокий"]
    for index, message in enumerate(result.chat.get("messages", [])):
        if message["role"] == "system":
            if message["text"].startswith(
                "Мы закончили опрос и готовы предоставить вам отчет"
            ):
                break
            _question = message["text"].split(". Возможные варианты ответа")
            if len(_question) > 1:
                _question = _question[0]
            question = get_questionи_by_text(db=db, text=_question)
            if question is not None:
                answer = result.chat.get("messages", [])[index + 1]
                for answer_obj in question.answers:
                    if answer_obj.answer == answer["text"]:
                        report += f"{question.question}\n**Уровень опасности: {sec_level[answer_obj.sec_value-1]}**\n "
    try:
        s = HTTPSession()
        r = s.post(
            "https://endless-presently-basilisk.ngrok-free.app/api/v1/chat/send_message/",
            json={"id": id, "message": result.repo},
        )
        response = r.json()
        update_system(
            db=db,
            id=id,
            user=user,
            update=SystemUpdate(report=report + response["text"]),
        )
        return report + response["text"]
    except Exception as err:
        print(err)
        return None
    return report
