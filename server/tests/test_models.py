import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.workout import Workout

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """Test creating a user."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active is True

@pytest.mark.asyncio
async def test_create_workout(db_session: AsyncSession):
    """Test creating a workout."""
    # First create a user
    user = User(
        email="workout_test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create a workout
    workout = Workout(
        user_id=user.id,
        name="Test Workout",
        description="Test workout description",
    )
    db_session.add(workout)
    await db_session.commit()
    await db_session.refresh(workout)

    assert workout.id is not None
    assert workout.name == "Test Workout"
    assert workout.user_id == user.id 