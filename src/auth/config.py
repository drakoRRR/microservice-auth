import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AuthConfig(BaseSettings):
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
