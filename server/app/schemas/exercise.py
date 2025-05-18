from app.schemas.base import NoWhitespaceString
from pydantic import BaseModel


class MuscleGroupBase(BaseModel):
    id: int
    name: NoWhitespaceString


class ExerciseBase(BaseModel):
    id: int
    name: NoWhitespaceString
    description: NoWhitespaceString
    aliases: list[NoWhitespaceString]
    muscle_group: MuscleGroupBase


class ExerciseDetail(ExerciseBase):
    pass


class ExerciseList(ExerciseBase):
    pass


class ExerciseSearchParams(BaseModel):
    search: NoWhitespaceString | None = None
    muscle_group: NoWhitespaceString | None = None
