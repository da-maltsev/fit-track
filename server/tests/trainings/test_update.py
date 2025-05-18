from datetime import UTC, datetime

from httpx import AsyncClient


async def test_update_training(as_user: AsyncClient, training, exercise):
    """Test updating a training."""
    update_data = {"date": datetime.now(UTC).isoformat(), "exercises": [{"exercise_id": exercise.id, "sets": 4, "reps": 12, "weight": 60.0}]}

    response = await as_user.put(f"/api/v1/trainings/{training.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == training.id
    assert len(data["exercises"]) == 1
    assert data["exercises"][0]["reps"] == 12
    assert data["exercises"][0]["weight"] == 60.0
    assert data["exercises"][0]["sets"] == 4


async def test_update_training_not_found(as_user: AsyncClient, training_data):
    """Test updating a non-existent training."""
    response = await as_user.put("/api/v1/trainings/999", json=training_data)
    assert response.status_code == 404
