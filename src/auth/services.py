from datetime import datetime, timedelta
from typing import Optional, Union

from src.auth.hashing import Hasher
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import AuthConfig
from src.config import Config
from src.dals import UserDAL
from src.models import User

from .schemas import ShowUser, UserCreate


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            username=body.username,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowUser(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )


async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(
            email=email,
        )


async def authenticate_user(
    email: str, password: str, db: AsyncSession
) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=AuthConfig().ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, Config().SECRET_KEY, algorithm=AuthConfig().ALGORITHM
    )
    return encoded_jwt
