from core.schema import SuccessResult
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Question
from schemas import QuestionCreate, QuestionRead, QuestionReadList, QuestionUpdate


def get_question(db: Session, id: int) -> QuestionRead:
    try:
        result = db.query(Question).filter(Question.id == id).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_questions(
    db: Session, offset: int = 0, limit: int | None = None
) -> list[QuestionReadList]:
    try:
        result = db.query(Question).offset(offset).limit(limit).all()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def create_question(db: Session, create: QuestionCreate) -> QuestionRead:
    try:
        db_instance = Question(**create.model_dump())
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def count_question(db: Session) -> int:
    try:
        result = db.query(Question.id).count()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result


def update_question(db: Session, id: int, update: QuestionUpdate) -> QuestionRead:
    try:
        db_instance: Question = get_question(db=db, id=id)
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


def find_question(db: Session, default: dict) -> QuestionRead | None:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(Question, key) == default.get(key, None))
        result = db.query(Question).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.first()


def find_questions(db: Session, default: dict) -> list[QuestionReadList]:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(Question, key) == default.get(key, None))
        result = db.query(Question).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.all()


def delete_question(db: Session, id: int) -> SuccessResult:
    try:
        db_instance = get_question(db=db, id=id)
        if not db_instance:
            raise HTTPException(status_code=404, detail="Record not found")
        db.delete(db_instance)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return SuccessResult(success=True)