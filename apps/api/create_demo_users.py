from core.database import get_db
from schemas import UserCreate
from services.user import create_user
from fastapi.exceptions import HTTPException

db = get_db().__next__()
try:
    print("Create admin user")
    create_user(
        db=db,
        create=UserCreate(
            email="admin@forpost.ru",
            password="admin",
            is_active=True,
            is_superuser=True,
            is_verified=True,
        ),
    )
except HTTPException:
    print("Admin user already exists")
try:
    print("Create user user")
    create_user(
        db=db,
        create=UserCreate(
            email="user@forpost.ru",
            password="user",
            is_active=True,
            is_superuser=False,
            is_verified=True,
        ),
    )
except HTTPException:
    print("Admin user already exists")
