from logging import getLogger

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.auth.schemas import UserCreate, ShowUser
from src.auth.services import _create_new_user

auth_router = APIRouter()

logger = getLogger(__name__)

@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Database error {err}")

