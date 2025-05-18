from app.schemas.base import NoWhitespaceString, PositiveInt
from pydantic import BaseModel


class MuscleGroupBase(BaseModel):
    id: PositiveInt
    name: NoWhitespaceString


class ExerciseBase(BaseModel):
    id: PositiveInt
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
