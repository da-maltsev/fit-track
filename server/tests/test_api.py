import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db_session: AsyncSession):
    """Test creating a user through the API."""
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "api_test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api_test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, db_session: AsyncSession):
    """Test getting a user through the API."""
    # First create a user
    user = User(
        email="get_test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    response = await client.get(f"/api/v1/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "get_test@example.com"
    assert data["id"] == user.id 