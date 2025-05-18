from typing import cast

from app.models.models import Exercise, Training, TrainingExercise
from app.schemas.training import TrainingCreate, TrainingUpdate
from fastapi import HTTPException
from sqlalchemy import Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class TrainingService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def get_training_query(self) -> Select:
        """Returns a base query for training with all necessary joins."""
        return select(Training).options(selectinload(Training.exercises).selectinload(TrainingExercise.exercise).selectinload(Exercise.muscle_group))

    async def get_training_by_id(
        self,
        training_id: int,
        user_id: int,
        include_exercises: bool = True,
    ) -> Training:
        """Get a training by ID and verify user ownership."""
        query = self.get_training_query() if include_exercises else select(Training)
        query = query.filter(
            Training.id == training_id,
            Training.user_id == user_id,
        )
        result = await self.db.execute(query)
        training = result.scalar_one_or_none()
        if not training:
            raise HTTPException(status_code=404, detail="Training not found")
        return training

    async def create_training(self, training: TrainingCreate, user_id: int) -> Training:
        db_training = Training(
            user_id=user_id,
            date=training.date,
        )
        self.db.add(db_training)
        await self.db.flush()

        for exercise in training.exercises:
            db_exercise = TrainingExercise(
                training_id=db_training.id,
                exercise_id=exercise.exercise_id,
                sets=exercise.sets,
                reps=exercise.reps,
                weight=exercise.weight,
            )
            self.db.add(db_exercise)

        await self.db.commit()
        await self.db.refresh(db_training)
        return db_training

    async def get_user_trainings(self, user_id: int) -> list[Training]:
        query = self.get_training_query().filter(Training.user_id == user_id)
        result = await self.db.execute(query.order_by(Training.date.desc()))
        return cast("list[Training]", result.scalars().all())

    async def update_training(self, training_id: int, user_id: int, training: TrainingUpdate) -> Training:
        db_training = await self.get_training_by_id(training_id, user_id)
        db_training.date = training.date  # type: ignore[assignment]

        delete_query = delete(TrainingExercise).filter(TrainingExercise.training_id == training_id)
        await self.db.execute(delete_query)

        for exercise in training.exercises:
            db_exercise = TrainingExercise(
                training_id=db_training.id,
                exercise_id=exercise.exercise_id,
                sets=exercise.sets,
                reps=exercise.reps,
                weight=exercise.weight,
            )
            self.db.add(db_exercise)

        await self.db.commit()
        await self.db.refresh(db_training)
        return db_training

    async def delete_training(self, training_id: int, user_id: int) -> None:
        training = await self.get_training_by_id(training_id, user_id, include_exercises=False)
        await self.db.delete(training)
        await self.db.commit()
