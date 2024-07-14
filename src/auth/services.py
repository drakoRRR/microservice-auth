from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from src.auth.dals import UserDAL
from src.auth.hashing import Hasher
from src.auth.models import TokenBlacklist, User
from src.config import SECRET_KEY
from src.database import get_db

from .schemas import ChangePassword, ShowUser, TokenData, UserCreate


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            user_name=body.user_name,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowUser(
            user_id=user.user_id,
            user_name=user.user_name,
            email=user.email,
            is_active=user.is_active,
        )


async def _update_user_password(user: User, body: ChangePassword, session: AsyncSession) -> ShowUser:
    if not session.in_transaction():
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.update_password(
                user=user,
                new_hashed_password=Hasher.get_password_hash(body.new_password)
            )
    else:
        user_dal = UserDAL(session)
        return await user_dal.update_password(
            user=user,
            new_hashed_password=Hasher.get_password_hash(body.new_password)
        )


async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    if not session.in_transaction():
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(
                email=email,
            )
    else:
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
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


async def is_token_blacklisted(token: str, db: AsyncSession) -> bool:
    result = await db.execute(select(TokenBlacklist).where(TokenBlacklist.token == token))
    blacklisted_token = result.scalars().first()
    return blacklisted_token is not None


async def get_current_user(token: str, session: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
    except (JWTError, ValidationError):
        raise credentials_exception

    if await is_token_blacklisted(token, session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been blacklisted",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_email(
        email=token_data.sub,
    )
    if user is None:
        raise credentials_exception
    return user


async def logout_func(token: str, db: AsyncSession):
    blacklisted_token = TokenBlacklist(token=token)
    db.add(blacklisted_token)
    await db.commit()
