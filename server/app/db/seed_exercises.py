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
            "name": "Жим лежа",
            "description": "Базовое упражнение, которое в первую очередь нацелено на грудные мышцы, а также прорабатывает плечи и трицепсы.",
            "muscle_group": "грудь",
            "aliases": ["Barbell Bench Press", "Flat Bench Press", "Жим лежа"],
        },
        {
            "name": "Приседания со штангой",
            "description": "Базовое упражнение, которое нацелено на квадрицепсы, бицепс бедра и ягодичные мышцы.",
            "muscle_group": "ноги",
            "aliases": ["Barbell Squat", "Back Squat", "Приседания со штангой"],
        },
        {
            "name": "Становая тяга",
            "description": "Базовое упражнение, которое прорабатывает всю заднюю цепь, включая спину, ягодицы и бицепс бедра.",
            "muscle_group": "спина",
            "aliases": ["Conventional Deadlift", "Становая тяга"],
        },
        {
            "name": "Подтягивания",
            "description": "Упражнение с собственным весом, которое в первую очередь нацелено на спину и бицепс.",
            "muscle_group": "спина",
            "aliases": ["Chin-up", "Подтягивания"],
        },
        {
            "name": "Жим штанги стоя",
            "description": "Базовое упражнение, которое нацелено на плечи и трицепсы.",
            "muscle_group": "плечи",
            "aliases": ["Military Press", "Standing Press", "Жим штанги стоя"],
        },
        {
            "name": "Тяга штанги в наклоне",
            "description": "Базовое упражнение, которое нацелено на мышцы спины.",
            "muscle_group": "спина",
            "aliases": ["Bent Over Row", "Тяга штанги в наклоне"],
        },
        {
            "name": "Жим гантелей лежа",
            "description": "Упражнение для груди, которое позволяет выполнять движение с большей амплитудой, чем жим штанги лежа.",
            "muscle_group": "грудь",
            "aliases": ["Dumbbell Bench Press", "Жим гантелей лежа"],
        },
        {
            "name": "Румынская тяга",
            "description": "Вариация становой тяги, которая больше фокусируется на бицепсе бедра и ягодичных мышцах.",
            "muscle_group": "ноги",
            "aliases": ["RDL", "Румынская тяга"],
        },
        {
            "name": "Выпады",
            "description": "Одностороннее упражнение для ног, которое нацелено на квадрицепсы, бицепс бедра и ягодичные мышцы.",
            "muscle_group": "ноги",
            "aliases": ["Walking Lunges", "Static Lunges", "Выпады"],
        },
        {
            "name": "Сгибание рук на бицепс",
            "description": "Изолирующее упражнение, которое нацелено на бицепс.",
            "muscle_group": "руки",
            "aliases": ["Dumbbell Curl", "Barbell Curl", "Сгибание рук на бицепс"],
        },
        {
            "name": "Разгибание рук на блоке",
            "description": "Изолирующее упражнение, которое нацелено на трицепс.",
            "muscle_group": "руки",
            "aliases": ["Cable Pushdown", "Разгибание рук на блоке"],
        },
        {
            "name": "Жим ногами",
            "description": "Базовое упражнение, которое нацелено на квадрицепсы, бицепс бедра и ягодичные мышцы.",
            "muscle_group": "ноги",
            "aliases": ["Squat Press", "Жим ногами"],
        },
        {
            "name": "Тяга верхнего блока",
            "description": "Базовое упражнение, которое нацелено на широчайшие мышцы спины и другие мышцы спины.",
            "muscle_group": "спина",
            "aliases": ["Wide Grip Pulldown", "Тяга верхнего блока"],
        },
        {
            "name": "Жим гантелей сидя",
            "description": "Базовое упражнение, которое нацелено на дельтовидные мышцы и трицепсы.",
            "muscle_group": "плечи",
            "aliases": ["Dumbbell Shoulder Press", "Жим гантелей сидя"],
        },
        {
            "name": "Подъемы на носки",
            "description": "Изолирующее упражнение, которое нацелено на икроножные мышцы.",
            "muscle_group": "ноги",
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
