from datetime import UTC, datetime

import pytest
from app.core.security import get_password_hash
from app.models import Exercise, MuscleGroup, Training, TrainingExercise, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_create_user(db_session: AsyncSession) -> None:
    """Test creating a user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    # Query trainings explicitly instead of using lazy loading
    result = await db_session.execute(select(Training).where(Training.user_id == user.id))
    trainings = result.scalars().all()

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert len(trainings) == 0
    assert user.created_at is not None
    assert user.updated_at is not None


async def test_user_unique_email_constraint(db_session: AsyncSession) -> None:
    user1 = User(
        email="unique@example.com",
        username="uniqueuser1",
        hashed_password=get_password_hash("password1"),
    )
    db_session.add(user1)
    await db_session.flush()

    user2 = User(
        email="unique@example.com",
        username="uniqueuser2",
        hashed_password=get_password_hash("password2"),
    )
    db_session.add(user2)
    with pytest.raises(Exception):
        await db_session.flush()
    await db_session.rollback()


async def test_user_unique_username_constraint(db_session: AsyncSession) -> None:
    user1 = User(
        email="unique2@example.com",
        username="uniqueuser",
        hashed_password=get_password_hash("password1"),
    )
    db_session.add(user1)
    await db_session.flush()

    user2 = User(
        email="another2@example.com",
        username="uniqueuser",
        hashed_password=get_password_hash("password2"),
    )
    db_session.add(user2)
    with pytest.raises(Exception):
        await db_session.flush()
    await db_session.rollback()


async def test_create_exercise(db_session: AsyncSession) -> None:
    """Test creating an exercise."""
    muscle_group = MuscleGroup(name="Chest")
    db_session.add(muscle_group)
    await db_session.flush()
    await db_session.refresh(muscle_group)

    exercise = Exercise(
        name="Bench Press",
        description="Classic chest exercise",
        muscle_group=muscle_group,
    )
    db_session.add(exercise)
    await db_session.flush()
    await db_session.refresh(exercise)

    # Query training_exercises explicitly instead of using lazy loading
    result = await db_session.execute(select(TrainingExercise).where(TrainingExercise.exercise_id == exercise.id))
    training_exercises = result.scalars().all()

    assert exercise.id is not None
    assert exercise.name == "Bench Press"
    assert exercise.description == "Classic chest exercise"
    assert exercise.muscle_group_id == muscle_group.id
    assert len(training_exercises) == 0
    assert exercise.created_at is not None
    assert exercise.updated_at is not None


async def test_create_training_with_exercises(db_session: AsyncSession) -> None:
    """Test creating a training with exercises."""
    # Create user
    user = User(
        email="training@example.com",
        username="traininguser",
        hashed_password=get_password_hash("trainingpassword"),
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    # Create muscle group first
    muscle_group = MuscleGroup(name="Legs")
    db_session.add(muscle_group)
    await db_session.flush()
    await db_session.refresh(muscle_group)

    # Create exercise
    exercise = Exercise(
        name="Squat",
        description="Leg exercise",
        muscle_group=muscle_group,
    )
    db_session.add(exercise)
    await db_session.flush()
    await db_session.refresh(exercise)

    # Create training
    training = Training(
        user_id=user.id,
        date=datetime.now(UTC),
    )
    db_session.add(training)
    await db_session.flush()
    await db_session.refresh(training)

    # Create training exercise
    training_exercise = TrainingExercise(
        training_id=training.id,
        exercise_id=exercise.id,
        sets=3,
        reps=10,
        weight=100.0,
    )
    db_session.add(training_exercise)
    await db_session.flush()
    await db_session.refresh(training_exercise)

    # Query relationships explicitly instead of using lazy loading
    result = await db_session.execute(select(TrainingExercise).where(TrainingExercise.training_id == training.id).join(Exercise))
    training_exercises = result.scalars().all()

    assert training.id is not None
    assert len(training_exercises) == 1
    assert training_exercises[0].exercise.name == "Squat"
    assert training_exercises[0].sets == 3
    assert training_exercises[0].reps == 10
    assert training_exercises[0].weight == 100.0
    assert training.created_at is not None
    assert training.updated_at is not None

    # Verify user relationship
    result = await db_session.execute(select(Training).where(Training.user_id == user.id))
    user_trainings = result.scalars().all()
    assert len(user_trainings) == 1
    assert user_trainings[0].id == training.id

    # Verify exercise relationship
    result = await db_session.execute(select(TrainingExercise).where(TrainingExercise.exercise_id == exercise.id))
    exercise_trainings = result.scalars().all()
    assert len(exercise_trainings) == 1
    assert exercise_trainings[0].training_id == training.id
