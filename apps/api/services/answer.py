from core.schema import SuccessResult
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Answer
from schemas import AnswerCreate, AnswerRead, AnswerReadList, AnswerUpdate


def get_answer(db: Session, id: int) -> AnswerRead:
    try:
        result = db.query(Answer).filter(Answer.id == id).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_answers(
    db: Session, offset: int = 0, limit: int | None = None
) -> list[AnswerReadList]:
    try:
        result = db.query(Answer).offset(offset).limit(limit).all()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def create_answer(db: Session, create: AnswerCreate) -> AnswerRead:
    try:
        db_instance = Answer(**create.model_dump())
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def count_answer(db: Session) -> int:
    try:
        result = db.query(Answer.id).count()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result


def update_answer(db: Session, id: int, update: AnswerUpdate) -> AnswerRead:
    try:
        db_instance: Answer = get_answer(db=db, id=id)
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


def find_answer(db: Session, default: dict) -> AnswerRead | None:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(Answer, key) == default.get(key, None))
        result = db.query(Answer).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.first()


def find_answers(db: Session, default: dict) -> list[AnswerReadList]:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(Answer, key) == default.get(key, None))
        result = db.query(Answer).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.all()


def delete_answer(db: Session, id: int) -> SuccessResult:
    try:
        db_instance = get_answer(db=db, id=id)
        if not db_instance:
            raise HTTPException(status_code=404, detail="Record not found")
        db.delete(db_instance)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return SuccessResult(success=True)