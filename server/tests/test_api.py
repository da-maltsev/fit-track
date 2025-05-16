from datetime import UTC, datetime

from app.models import User
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_create_user(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test creating a user through the API."""
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "api_test@example.com",
            "username": "apitestuser",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api_test@example.com"
    assert data["username"] == "apitestuser"
    assert "id" in data


async def test_get_user(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test getting a user through the API."""
    # First create a user
    user = User(
        email="get_test@example.com",
        username="gettestuser",
        hashed_password="hashed_password",
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    response = await client.get(f"/api/v1/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "get_test@example.com"
    assert data["username"] == "gettestuser"
    assert data["id"] == user.id
