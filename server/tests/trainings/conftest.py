from datetime import UTC, datetime

import pytest
from app.models.models import Training, TrainingExercise
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def training_data(exercise):
    return {
        "date": datetime.now(UTC).isoformat(),
        "exercises": [{"exercise_id": exercise.id, "sets": 3, "reps": 10, "weight": 50.0}, {"exercise_id": exercise.id, "sets": 4, "reps": 12, "weight": 30.0}],
    }


@pytest.fixture
async def training(db_session: AsyncSession, user, exercise) -> Training:
    """Create a test training."""
    training = Training(
        user_id=user.id,
        date=datetime.now(UTC),
    )
    db_session.add(training)
    await db_session.flush()

    training_exercise = TrainingExercise(training_id=training.id, exercise_id=exercise.id, sets=3, reps=10, weight=50.0)
    db_session.add(training_exercise)
    await db_session.commit()
    await db_session.refresh(training)
    return training
