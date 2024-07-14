from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import ShowUser, UserCreate
from src.auth.services import _create_new_user
from src.database import get_db

auth_router = APIRouter()

logger = getLogger(__name__)

@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await _create_new_user(body, db)
        return new_user
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Database error {err}")

