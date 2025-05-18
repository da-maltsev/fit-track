from app.api.v1.endpoints import exercises, trainings, users
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(trainings.router, prefix="/trainings", tags=["trainings"])
