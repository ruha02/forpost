from core.schema import SuccessResult
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import System
from schemas import SystemCreate, SystemRead, SystemReadList, SystemUpdate


def get_system(db: Session, id: int) -> SystemRead:
    try:
        result = db.query(System).filter(System.id == id).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_systems(
    db: Session, offset: int = 0, limit: int | None = None
) -> list[SystemReadList]:
    try:
        result = db.query(System).offset(offset).limit(limit).all()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def create_system(db: Session, create: SystemCreate) -> SystemRead:
    try:
        db_instance = System(**create.model_dump())
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def count_system(db: Session) -> int:
    try:
        result = db.query(System.id).count()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result


def update_system(db: Session, id: int, update: SystemUpdate) -> SystemRead:
    try:
        db_instance: System = get_system(db=db, id=id)
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


def find_system(db: Session, default: dict) -> SystemRead | None:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(System, key) == default.get(key, None))
        result = db.query(System).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.first()


def find_systems(db: Session, default: dict) -> list[SystemReadList]:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(System, key) == default.get(key, None))
        result = db.query(System).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.all()


def delete_system(db: Session, id: int) -> SuccessResult:
    try:
        db_instance = get_system(db=db, id=id)
        if not db_instance:
            raise HTTPException(status_code=404, detail="Record not found")
        db.delete(db_instance)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return SuccessResult(success=True)