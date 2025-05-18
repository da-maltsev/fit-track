from app.models.models import Exercise, MuscleGroup
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_list_exercises(
    client: AsyncClient,
    db_session: AsyncSession,
    muscle_group: MuscleGroup,
    exercise: Exercise,
) -> None:
    """Test listing exercises."""
    response = await client.get("/api/v1/exercises/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == exercise.id
    assert data[0]["name"] == exercise.name


async def test_search_exercises_by_name(
    client: AsyncClient,
    db_session: AsyncSession,
    muscle_group: MuscleGroup,
    exercise: Exercise,
) -> None:
    """Test searching exercises by name."""
    response = await client.get("/api/v1/exercises/?search=test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == exercise.id


async def test_search_exercises_by_alias(
    client: AsyncClient,
    db_session: AsyncSession,
    muscle_group: MuscleGroup,
    exercise: Exercise,
) -> None:
    """Test searching exercises by alias."""
    response = await client.get("/api/v1/exercises/?search=alias")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == exercise.id


async def test_filter_exercises_by_muscle_group(
    client: AsyncClient,
    db_session: AsyncSession,
    muscle_group: MuscleGroup,
    exercise: Exercise,
) -> None:
    """Test filtering exercises by muscle group."""
    response = await client.get(f"/api/v1/exercises/?muscle_group={muscle_group.name}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == exercise.id
    assert data[0]["muscle_group"]["name"] == muscle_group.name
