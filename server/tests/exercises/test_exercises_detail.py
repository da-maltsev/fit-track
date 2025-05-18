from app.models.models import Exercise, MuscleGroup
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_exercise_detail(
    client: AsyncClient,
    db_session: AsyncSession,
    muscle_group: MuscleGroup,
    exercise: Exercise,
) -> None:
    """Test getting exercise details."""
    response = await client.get(f"/api/v1/exercises/{exercise.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == exercise.id
    assert data["name"] == exercise.name
    assert data["description"] == exercise.description
    assert data["muscle_group"]["id"] == muscle_group.id
    assert data["muscle_group"]["name"] == muscle_group.name


async def test_get_nonexistent_exercise(
    client: AsyncClient,
) -> None:
    """Test getting a nonexistent exercise."""
    response = await client.get("/api/v1/exercises/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise with id 999 not found"
