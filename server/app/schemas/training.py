from datetime import datetime
from typing import Self

from app.models.models import Exercise, Training, TrainingExercise
from app.schemas.base import PositiveFloat, PositiveInt
from pydantic import BaseModel, ConfigDict


class TrainingExerciseBase(BaseModel):
    exercise_id: PositiveInt
    sets: PositiveInt
    reps: PositiveInt
    weight: PositiveFloat

    @classmethod
    def from_orm(cls, obj: TrainingExercise) -> Self:
        return cls(
            exercise_id=obj.exercise_id,
            sets=obj.sets,
            reps=obj.reps,
            weight=obj.weight,
        )


class TrainingExerciseCreate(TrainingExerciseBase):
    pass


class ExerciseInfo(BaseModel):
    name: str
    muscle_group: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj: Exercise) -> Self:
        return cls(
            name=obj.name,
            muscle_group=obj.muscle_group.name,
        )


class TrainingExerciseRead(TrainingExerciseBase):
    id: PositiveInt
    training_id: PositiveInt
    exercise: ExerciseInfo

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj: TrainingExercise) -> Self:
        return cls(
            id=obj.id,
            training_id=obj.training_id,
            exercise_id=obj.exercise_id,
            sets=obj.sets,
            reps=obj.reps,
            weight=obj.weight,
            exercise=ExerciseInfo.from_orm(obj.exercise),
        )


class TrainingBase(BaseModel):
    date: datetime

    @classmethod
    def from_orm(cls, obj: Training) -> Self:
        return cls(date=obj.date)  # type: ignore[arg-type]


class TrainingCreate(TrainingBase):
    exercises: list[TrainingExerciseCreate]

    @classmethod
    def from_orm(cls, obj: Training) -> Self:
        return cls(
            date=obj.date,  # type: ignore[arg-type]
            exercises=[TrainingExerciseCreate.from_orm(te) for te in obj.exercises],
        )


class TrainingUpdate(TrainingBase):
    exercises: list[TrainingExerciseCreate]

    @classmethod
    def from_orm(cls, obj: Training) -> Self:
        return cls(
            date=obj.date,  # type: ignore[arg-type]
            exercises=[TrainingExerciseCreate.from_orm(te) for te in obj.exercises],
        )


class TrainingRead(TrainingBase):
    id: PositiveInt
    user_id: PositiveInt
    exercises: list[TrainingExerciseRead]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj: Training) -> Self:
        return cls(
            id=obj.id,
            user_id=obj.user_id,
            date=obj.date,  # type: ignore[arg-type]
            exercises=[TrainingExerciseRead.from_orm(te) for te in obj.exercises],
        )
