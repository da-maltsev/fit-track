from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    trainings: Mapped[list["Training"]] = relationship("Training", back_populates="user")


class MuscleGroup(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    exercises: Mapped[list["Exercise"]] = relationship("Exercise", back_populates="muscle_group")


class Exercise(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    muscle_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("musclegroup.id"), index=True)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list, index=True)

    training_exercises: Mapped[list["TrainingExercise"]] = relationship("TrainingExercise", back_populates="exercise")
    muscle_group: Mapped["MuscleGroup"] = relationship("MuscleGroup", back_populates="exercises")


class Training(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True)

    user: Mapped["User"] = relationship("User", back_populates="trainings")
    exercises: Mapped[list["TrainingExercise"]] = relationship("TrainingExercise", back_populates="training", cascade="all, delete-orphan")


class TrainingExercise(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    training_id: Mapped[int] = mapped_column(Integer, ForeignKey("training.id"))
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercise.id"))
    sets: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)

    training: Mapped["Training"] = relationship("Training", back_populates="exercises")
    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="training_exercises")
