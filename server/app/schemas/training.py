from datetime import datetime

from app.schemas.base import PositiveFloat, PositiveInt
from pydantic import BaseModel


class TrainingExerciseBase(BaseModel):
    exercise_id: PositiveInt
    sets: PositiveInt
    reps: PositiveInt
    weight: PositiveFloat


class TrainingExerciseCreate(TrainingExerciseBase):
    pass


class TrainingExerciseRead(TrainingExerciseBase):
    id: PositiveInt
    training_id: PositiveInt

    class Config:
        from_attributes = True


class TrainingBase(BaseModel):
    date: datetime


class TrainingCreate(TrainingBase):
    exercises: list[TrainingExerciseCreate]


class TrainingUpdate(TrainingBase):
    exercises: list[TrainingExerciseCreate]


class TrainingRead(TrainingBase):
    id: PositiveInt
    user_id: PositiveInt
    exercises: list[TrainingExerciseRead]

    class Config:
        from_attributes = True
