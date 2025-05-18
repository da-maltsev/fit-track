from typing import Annotated

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.schemas.training import TrainingCreate, TrainingRead, TrainingUpdate
from app.services.training_service import TrainingService
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/")
async def create_training(
    training: TrainingCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TrainingRead:
    service = TrainingService(db)
    db_training = await service.create_training(training, current_user.id)
    db_training = await service.get_training_by_id(db_training.id, current_user.id)
    return TrainingRead.from_orm(db_training)


@router.get("/")
async def read_trainings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[TrainingRead]:
    service = TrainingService(db)
    trainings = await service.get_user_trainings(current_user.id)
    return [TrainingRead.from_orm(training) for training in trainings]


@router.get("/{training_id}")
async def read_training(
    training_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TrainingRead:
    service = TrainingService(db)
    training = await service.get_training_by_id(training_id, current_user.id)
    return TrainingRead.from_orm(training)


@router.put("/{training_id}")
async def update_training(
    training_id: int,
    training: TrainingUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TrainingRead:
    service = TrainingService(db)
    await service.update_training(training_id, current_user.id, training)
    db_training = await service.get_training_by_id(training_id, current_user.id)
    return TrainingRead.from_orm(db_training)


@router.delete("/{training_id}")
async def delete_training(
    training_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    service = TrainingService(db)
    await service.delete_training(training_id, current_user.id)
    return {"message": "Training deleted successfully"}
