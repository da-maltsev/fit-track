from typing import Annotated

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.models import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services import user as user_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/")
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """Create a new user."""
    db_user = await user_service.create_user(db, user_data)
    return UserResponse.model_validate(db_user)


@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Get current user information."""
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """Get a user by ID."""
    db_user = await user_service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(db_user)


@router.post("/login")
async def login(
    user_data: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """Login a user."""
    user = await user_service.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token)
