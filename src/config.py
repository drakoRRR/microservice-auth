import os
import pathlib

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """Global config project."""
    BASE_DIR: str = str(pathlib.Path(__file__).parent)

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", default="postgres")
    DB_HOST: str = os.getenv("DB_HOST", default="0.0.0.0")
    DB_PORT: str = os.getenv("DB_PORT", default="5432")
    DB_NAME: str = os.getenv("DB_NAME", default="db")

    DATABASE_URL: PostgresDsn = \
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DEBUG: bool = bool(os.getenv("DEBUG", default=True))
    SECRET_KEY: str = os.getenv("SECRET_KEY", default="secret-key")
    APP_PORT: int = os.getenv("APP_PORT", default=8000)

