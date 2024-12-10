from core.schema import SuccessResult
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserRead, UserReadList, UserUpdate
from .auth import PWD_CONTEXT


def get_user(db: Session, id: int) -> UserRead:
    try:
        result = db.query(User).filter(User.id == id).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_user_by_email(db: Session, email: str) -> UserRead:
    try:
        result = db.query(User).filter(User.email == email).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_users(
    db: Session, offset: int = 0, limit: int | None = None
) -> list[UserReadList]:
    try:
        result = db.query(User).offset(offset).limit(limit).all()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def create_user(db: Session, create: UserCreate) -> UserRead:
    if get_user_by_email(db, create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    d_user = create.model_dump()
    d_user["hashed_password"] = PWD_CONTEXT.hash(create.password)
    del d_user["password"]
    db_user = User(**d_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserRead.model_validate(db_user)


def count_user(db: Session) -> int:
    try:
        result = db.query(User.id).count()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result


def update_user(db: Session, id: int, update: UserUpdate) -> UserRead:
    try:
        db_instance: User = get_user(db=db, id=id)
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


def find_user(db: Session, default: dict) -> UserRead | None:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(User, key) == default.get(key, None))
        result = db.query(User).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.first()


def find_users(db: Session, default: dict) -> list[UserReadList]:
    try:
        statements = list()
        for key in list(default.keys()):
            statements.append(getattr(User, key) == default.get(key, None))
        result = db.query(User).where(*statements)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return result.all()


def delete_user(db: Session, id: int) -> SuccessResult:
    try:
        db_instance = get_user(db=db, id=id)
        if not db_instance:
            raise HTTPException(status_code=404, detail="Record not found")
        db.delete(db_instance)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return SuccessResult(success=True)
