from httpx import AsyncClient


async def test_create_training(as_user: AsyncClient, training_data, exercise):
    """Test creating a new training."""
    # Update exercise_id to match the test exercise
    training_data["exercises"][0]["exercise_id"] = exercise.id

    response = await as_user.post("/api/v1/trainings/", json=training_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] is not None
    assert len(data["exercises"]) == len(training_data["exercises"])
    assert data["exercises"][0]["exercise_id"] == exercise.id
    assert data["exercises"][0]["sets"] == 3
    assert data["exercises"][0]["reps"] == 10
    assert data["exercises"][0]["weight"] == 50.0


async def test_create_training_unauthorized(as_anon: AsyncClient, training_data):
    """Test creating a training without authentication."""
    response = await as_anon.post("/api/v1/trainings/", json=training_data)
    assert response.status_code == 401
