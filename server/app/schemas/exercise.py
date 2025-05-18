from pydantic import BaseModel


class MuscleGroupBase(BaseModel):
    id: int
    name: str


class ExerciseBase(BaseModel):
    id: int
    name: str
    description: str
    aliases: list[str]
    muscle_group: MuscleGroupBase


class ExerciseDetail(ExerciseBase):
    pass


class ExerciseList(ExerciseBase):
    pass


class ExerciseSearchParams(BaseModel):
    search: str | None = None
    muscle_group: str | None = None
