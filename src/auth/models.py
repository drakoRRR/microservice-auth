import uuid

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class User(Base):
    """User model representing users in the application."""
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class TokenBlacklist(Base):
    """Token blacklist model representing tokens in the application."""
    __tablename__ = "token_blacklist"

    token = Column(String, primary_key=True, index=True)
    blacklisted_on = Column(DateTime, default=func.now())
