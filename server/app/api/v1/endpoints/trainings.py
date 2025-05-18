from typing import Annotated

from app.api.deps import get_current_user, get_db
from app.models.models import Training, TrainingExercise, User
from app.schemas.training import TrainingCreate, TrainingRead, TrainingUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


router = APIRouter()


@router.post("/")
async def create_training(
    training: TrainingCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TrainingRead:
    db_training = Training(
        user_id=current_user.id,
        date=training.date,
    )
    db.add(db_training)
    await db.flush()

    for exercise in training.exercises:
        db_exercise = TrainingExercise(
            training_id=db_training.id,
            exercise_id=exercise.exercise_id,
            sets=exercise.sets,
            reps=exercise.reps,
            weight=exercise.weight,
        )
        db.add(db_exercise)

    await db.commit()
    await db.refresh(db_training)

    # Reload training with relationships
    query = select(Training).options(selectinload(Training.exercises).selectinload(TrainingExercise.exercise)).where(Training.id == db_training.id)
    result = await db.execute(query)
    db_training = result.scalar_one()
    return TrainingRead.model_validate(db_training)


@router.get("/")
async def read_trainings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[TrainingRead]:
    query = select(Training).options(selectinload(Training.exercises).selectinload(TrainingExercise.exercise)).filter(Training.user_id == current_user.id)
    result = await db.execute(query)
    trainings = result.scalars().all()
    return [TrainingRead.model_validate(training) for training in trainings]


@router.get("/{training_id}")
async def read_training(
    training_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TrainingRead:
    query = (
        select(Training)
        .options(selectinload(Training.exercises).selectinload(TrainingExercise.exercise))
        .filter(
            Training.id == training_id,
            Training.user_id == current_user.id,
        )
    )
    result = await db.execute(query)
    training = result.scalar_one_or_none()
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    return TrainingRead.model_validate(training)


@router.put("/{training_id}")
async def update_training(
    training_id: int,
    training: TrainingUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TrainingRead:
    query = (
        select(Training)
        .options(selectinload(Training.exercises).selectinload(TrainingExercise.exercise))
        .filter(
            Training.id == training_id,
            Training.user_id == current_user.id,
        )
    )
    result = await db.execute(query)
    db_training = result.scalar_one_or_none()
    if not db_training:
        raise HTTPException(status_code=404, detail="Training not found")

    db_training.date = training.date  # type: ignore[assignment]

    # Delete existing exercises
    delete_query = delete(TrainingExercise).filter(TrainingExercise.training_id == training_id)
    await db.execute(delete_query)

    # Add new exercises
    for exercise in training.exercises:
        db_exercise = TrainingExercise(
            training_id=db_training.id,
            exercise_id=exercise.exercise_id,
            sets=exercise.sets,
            reps=exercise.reps,
            weight=exercise.weight,
        )
        db.add(db_exercise)

    await db.commit()
    await db.refresh(db_training)

    # Reload training with relationships
    query = select(Training).options(selectinload(Training.exercises).selectinload(TrainingExercise.exercise)).where(Training.id == db_training.id)
    result = await db.execute(query)
    db_training = result.scalar_one()
    return TrainingRead.model_validate(db_training)


@router.delete("/{training_id}")
async def delete_training(
    training_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    query = select(Training).filter(
        Training.id == training_id,
        Training.user_id == current_user.id,
    )
    result = await db.execute(query)
    training = result.scalar_one_or_none()
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")

    await db.delete(training)
    await db.commit()
    return {"message": "Training deleted successfully"}
