from typing import TypedDict

from app.models.models import Exercise, MuscleGroup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ExerciseData(TypedDict):
    name: str
    description: str
    muscle_group: str
    aliases: list[str]


async def get_or_create_muscle_group(db: AsyncSession, name: str) -> MuscleGroup:
    """Get existing muscle group or create a new one."""
    stmt = select(MuscleGroup).where(MuscleGroup.name == name)
    result = await db.execute(stmt)
    muscle_group = result.scalar_one_or_none()

    if muscle_group is None:
        muscle_group = MuscleGroup(name=name)
        db.add(muscle_group)
        await db.commit()
        await db.refresh(muscle_group)

    return muscle_group


async def get_or_create_exercise(
    db: AsyncSession,
    name: str,
    description: str,
    muscle_group_name: str,
    aliases: list[str],
) -> Exercise:
    """Get existing exercise or create a new one."""
    stmt = select(Exercise).where(Exercise.name == name)
    result = await db.execute(stmt)
    exercise = result.scalar_one_or_none()

    if exercise is None:
        muscle_group = await get_or_create_muscle_group(db, muscle_group_name)
        exercise = Exercise(
            name=name,
            description=description,
            muscle_group_id=muscle_group.id,
            aliases=aliases,
        )
        db.add(exercise)
        await db.commit()
        await db.refresh(exercise)

    return exercise


async def seed_exercises(db: AsyncSession) -> None:
    """Seed the database with common gym exercises."""
    exercises_data: list[ExerciseData] = [
        {
            "name": "Bench Press",
            "description": "A compound exercise that primarily targets the chest muscles, also working the shoulders and triceps.",
            "muscle_group": "chest",
            "aliases": ["Barbell Bench Press", "Flat Bench Press", "Жим лежа"],
        },
        {
            "name": "Squat",
            "description": "A compound exercise that targets the quadriceps, hamstrings, and glutes.",
            "muscle_group": "legs",
            "aliases": ["Barbell Squat", "Back Squat", "Приседания со штангой"],
        },
        {
            "name": "Deadlift",
            "description": "A compound exercise that works the entire posterior chain, including the back, glutes, and hamstrings.",
            "muscle_group": "back",
            "aliases": ["Conventional Deadlift", "Становая тяга"],
        },
        {
            "name": "Pull-up",
            "description": "A bodyweight exercise that primarily targets the back and biceps.",
            "muscle_group": "back",
            "aliases": ["Chin-up", "Подтягивания"],
        },
        {
            "name": "Overhead Press",
            "description": "A compound exercise that targets the shoulders and triceps.",
            "muscle_group": "shoulders",
            "aliases": ["Military Press", "Standing Press", "Жим штанги стоя"],
        },
        {
            "name": "Barbell Row",
            "description": "A compound exercise that targets the back muscles.",
            "muscle_group": "back",
            "aliases": ["Bent Over Row", "Тяга штанги в наклоне"],
        },
        {
            "name": "Dumbbell Press",
            "description": "A chest exercise that allows for greater range of motion than the barbell bench press.",
            "muscle_group": "chest",
            "aliases": ["Dumbbell Bench Press", "Жим гантелей лежа"],
        },
        {
            "name": "Romanian Deadlift",
            "description": "A variation of the deadlift that focuses more on the hamstrings and glutes.",
            "muscle_group": "legs",
            "aliases": ["RDL", "Румынская тяга"],
        },
        {
            "name": "Lunges",
            "description": "A unilateral leg exercise that targets the quadriceps, hamstrings, and glutes.",
            "muscle_group": "legs",
            "aliases": ["Walking Lunges", "Static Lunges", "Выпады"],
        },
        {
            "name": "Bicep Curl",
            "description": "An isolation exercise that targets the biceps.",
            "muscle_group": "arms",
            "aliases": ["Dumbbell Curl", "Barbell Curl", "Сгибание рук на бицепс"],
        },
        {
            "name": "Tricep Pushdown",
            "description": "An isolation exercise that targets the triceps.",
            "muscle_group": "arms",
            "aliases": ["Cable Pushdown", "Разгибание рук на блоке"],
        },
        {
            "name": "Leg Press",
            "description": "A compound exercise that targets the quadriceps, hamstrings, and glutes.",
            "muscle_group": "legs",
            "aliases": ["Squat Press", "Жим ногами"],
        },
        {
            "name": "Lat Pulldown",
            "description": "A compound exercise that targets the latissimus dorsi and other back muscles.",
            "muscle_group": "back",
            "aliases": ["Wide Grip Pulldown", "Тяга верхнего блока"],
        },
        {
            "name": "Shoulder Press",
            "description": "A compound exercise that targets the deltoids and triceps.",
            "muscle_group": "shoulders",
            "aliases": ["Dumbbell Shoulder Press", "Жим гантелей сидя"],
        },
        {
            "name": "Calf Raise",
            "description": "An isolation exercise that targets the calf muscles.",
            "muscle_group": "legs",
            "aliases": ["Standing Calf Raise", "Подъемы на носки", "Единорог"],
        },
    ]

    for exercise_data in exercises_data:
        await get_or_create_exercise(
            db,
            name=exercise_data["name"],
            description=exercise_data["description"],
            muscle_group_name=exercise_data["muscle_group"],
            aliases=exercise_data["aliases"],
        )
