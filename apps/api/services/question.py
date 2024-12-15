from core.schema import SuccessResult
from fastapi import HTTPException, status
from filters import QuestionFilter
from models import Answer, Question
from schemas import QuestionCreate, QuestionRead, QuestionReadList, QuestionUpdate
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def get_question(db: Session, id: int) -> QuestionRead:
    try:
        result = db.query(Question).filter(Question.id == id).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_questions(
    db: Session,
    offset: int = 0,
    limit: int | None = None,
    filter: QuestionFilter = None,
) -> list[QuestionReadList]:
    try:
        query = filter.filter(db.query(Question).order_by(Question.id))
        result = db.execute(query).scalars().all()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result[offset : (offset + limit)] if limit else result[offset:]


def create_question(db: Session, create: QuestionCreate) -> QuestionRead:
    try:
        data = create.model_dump()
        answers_data = data.pop("answers", [])

        db_instance = Question(**data)
        db.add(db_instance)
        db.flush()

        for answer_data in answers_data:
            answer = Answer(**answer_data, question_id=db_instance.id)
            db.add(answer)

        db.commit()
        db.refresh(db_instance)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def count_question(db: Session, filter: QuestionFilter) -> int:
    try:
        query = filter.filter(select(func.count(Question.id)))
        result = db.execute(query).scalars().one()
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
        answers_data = update_data.pop("answers", None)

        for key, value in update_data.items():
            setattr(db_instance, key, value)

        if answers_data:
            existing_answers = {answer.id: answer for answer in db_instance.answers}
            incoming_answer_ids = {a.get("id") for a in answers_data if a.get("id")}
            for answer_id in existing_answers:
                if answer_id not in incoming_answer_ids:
                    db.delete(existing_answers[answer_id])
            for answer_data in answers_data:
                answer_id = answer_data.get("id")
                if answer_id and answer_id in existing_answers:
                    for key, value in answer_data.items():
                        setattr(existing_answers[answer_id], key, value)
                else:
                    new_answer = Answer(**answer_data, question_id=id)
                    db.add(new_answer)

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
