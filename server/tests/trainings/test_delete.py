from httpx import AsyncClient


async def test_delete_training(as_user: AsyncClient, training):
    """Test deleting a training."""
    response = await as_user.delete(f"/api/v1/trainings/{training.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Training deleted successfully"

    # Verify training is deleted
    get_response = await as_user.get(f"/api/v1/trainings/{training.id}")
    assert get_response.status_code == 404


async def test_delete_training_not_found(as_user: AsyncClient):
    """Test deleting a non-existent training."""
    response = await as_user.delete("/api/v1/trainings/999")
    assert response.status_code == 404
