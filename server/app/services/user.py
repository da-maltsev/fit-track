from datetime import UTC, datetime

from app.core.security import get_password_hash
from app.models.models import User
from app.schemas.user import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user."""
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        updated_at=datetime.now(UTC),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    """Get a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
