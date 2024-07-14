import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    user_name: str
    email: EmailStr
    is_active: bool


class UserCreate(TunedModel):
    name: str
    user_name: str
    email: EmailStr
    password: str


class Token(TunedModel):
    access_token: str
    token_type: str


class ChangePassword(TunedModel):
    old_password: str
    new_password: str


class TokenData(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
