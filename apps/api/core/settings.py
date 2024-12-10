from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    app_name: str = "ФОРПОСТ"
    version: str = "1.0.0"
    api_prefix: str = "/api"

    # Database settings
    database_url: str = os.getenv("DATABASE_URL")

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = 30


@lru_cache
def get_settings():
    return Settings()
