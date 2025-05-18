from httpx import AsyncClient


async def test_get_trainings(as_user: AsyncClient, training):
    """Test getting all trainings for the current user."""
    response = await as_user.get("/api/v1/trainings/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == training.id
    assert len(data[0]["exercises"]) == 1


async def test_get_training(as_user: AsyncClient, training, training_data):
    """Test getting a specific training."""
    response = await as_user.get(f"/api/v1/trainings/{training.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == training.id
    assert len(data["exercises"]) == 1
    assert data["exercises"][0]["exercise_id"] == training_data["exercises"][0]["exercise_id"]


async def test_get_training_not_found(as_user: AsyncClient):
    """Test getting a non-existent training."""
    response = await as_user.get("/api/v1/trainings/999")
    assert response.status_code == 404
