from app.models.models import Exercise, MuscleGroup
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_exercise_detail(
    as_user: AsyncClient,
    db_session: AsyncSession,
    muscle_group: MuscleGroup,
    exercise: Exercise,
) -> None:
    """Test getting exercise details."""
    response = await as_user.get(f"/api/v1/exercises/{exercise.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == exercise.id
    assert data["name"] == exercise.name
    assert data["description"] == exercise.description
    assert data["muscle_group"]["id"] == muscle_group.id
    assert data["muscle_group"]["name"] == muscle_group.name


async def test_get_nonexistent_exercise(
    as_user: AsyncClient,
) -> None:
    """Test getting a nonexistent exercise."""
    response = await as_user.get("/api/v1/exercises/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise with id 999 not found"


async def test_get_exercise_detail_unauthorized(
    as_anon: AsyncClient,
    exercise: Exercise,
) -> None:
    """Test getting exercise details without authentication."""
    response = await as_anon.get(f"/api/v1/exercises/{exercise.id}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
