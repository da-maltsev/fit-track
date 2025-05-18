from typing import Annotated

from app.api.deps import get_db
from app.models.models import Exercise, MuscleGroup
from app.schemas.exercise import ExerciseDetail, ExerciseList, ExerciseSearchParams
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


router = APIRouter()


@router.get("/{exercise_id}", response_model=ExerciseDetail)
async def get_exercise(
    exercise_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Exercise:
    """Get exercise details by ID."""
    query = select(Exercise).options(selectinload(Exercise.muscle_group)).where(Exercise.id == exercise_id)
    result = await db.execute(query)
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail=f"Exercise with id {exercise_id} not found")
    return exercise


@router.get("/", response_model=list[ExerciseList])
async def list_exercises(
    search_params: Annotated[ExerciseSearchParams, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Exercise]:
    """List exercises with optional search and filtering."""
    query = select(Exercise).options(selectinload(Exercise.muscle_group))

    if search_params.search:
        search_term = f"%{search_params.search}%"
        query = query.where((Exercise.name.ilike(search_term)) | (Exercise.aliases.cast(str).ilike(search_term)))

    if search_params.muscle_group:
        query = query.join(MuscleGroup).where(MuscleGroup.name.ilike(f"%{search_params.muscle_group}%"))

    result = await db.execute(query.order_by(Exercise.name))
    return list(result.scalars().all())
