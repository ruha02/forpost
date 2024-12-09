from core.schema import SuccessResult
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Source
from schemas import SourceCreate, SourceRead, SourceReadList, SourceUpdate


def get_source(db: Session, id: int) -> SourceRead:
    try:
        result = db.query(Source).filter(Source.id == id).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_sources(
    db: Session, offset: int = 0, limit: int | None = None
) -> list[SourceReadList]:
    try:
        result = db.query(Source).offset(offset).limit(limit).all()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def create_source(db: Session, create: SourceCreate) -> SourceRead:
    try:
        db_instance = Source(**create.model_dump())
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def count_source(db: Session) -> int:
    try:
        result = db.query(Source.id).count()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result


def update_source(db: Session, id: int, update: SourceUpdate) -> SourceRead:
    try:
        db_instance: Source = get_source(db=db, id=id)
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


def find_source(db: Session, default: dict) -> SourceRead | None:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(Source, key) == default.get(key, None))
        result = db.query(Source).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.first()


def find_sources(db: Session, default: dict) -> list[SourceReadList]:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(Source, key) == default.get(key, None))
        result = db.query(Source).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.all()


def delete_source(db: Session, id: int) -> SuccessResult:
    try:
        db_instance = get_source(db=db, id=id)
        if not db_instance:
            raise HTTPException(status_code=404, detail="Record not found")
        db.delete(db_instance)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return SuccessResult(success=True)