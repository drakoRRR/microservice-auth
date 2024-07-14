from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.models import User
from src.auth.schemas import ChangePassword, ShowUser, Token
from src.auth.services import (_update_user_password, authenticate_user,
                               create_access_token, get_current_user,
                               logout_func)
from src.database import get_db

login_router = APIRouter()


@login_router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@login_router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(change_password_data: ChangePassword, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    user = await authenticate_user(current_user.email, change_password_data.old_password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    await _update_user_password(user, change_password_data, db)
    return {"msg": "Password changed successfully"}


@login_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str, db: AsyncSession = Depends(get_db)):
    await logout_func(token, db)
    return {"msg": "Successfully logged out"}


@login_router.get("/check-login", status_code=status.HTTP_200_OK)
async def check_login_status(current_user: User = Depends(get_current_user)):
    return {"msg": "You are logged in", "user": ShowUser.from_orm(current_user)}
