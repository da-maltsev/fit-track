import pytest
from app.models import User
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_create_user(as_anon: AsyncClient, db_session: AsyncSession) -> None:
    """Test creating a user through the API."""
    response = await as_anon.post(
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


async def test_get_user(as_anon: AsyncClient, db_session: AsyncSession, user: User) -> None:
    """Test getting a user through the API."""
    response = await as_anon.get(f"/api/v1/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["username"] == user.username
    assert data["id"] == user.id


@pytest.mark.parametrize("field_name", ["username", "email"])
async def test_login_success(as_anon: AsyncClient, db_session: AsyncSession, user: User, field_name: str) -> None:
    """Test successful login through the API."""
    response = await as_anon.post(
        "/api/v1/users/login",
        json={
            "username": getattr(user, field_name),
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(as_anon: AsyncClient, db_session: AsyncSession, user: User) -> None:
    """Test login with wrong password through the API."""
    response = await as_anon.post(
        "/api/v1/users/login",
        json={
            "username": user.username,
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


async def test_login_nonexistent_user(as_anon: AsyncClient, db_session: AsyncSession) -> None:
    """Test login with nonexistent user through the API."""
    response = await as_anon.post(
        "/api/v1/users/login",
        json={
            "username": "nonexistent@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


async def test_get_current_user(as_user: AsyncClient, user: User) -> None:
    """Test getting current user information through the API."""
    response = await as_user.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["username"] == user.username
    assert data["id"] == user.id


async def test_get_current_user_no_token(as_anon: AsyncClient) -> None:
    """Test getting current user without token."""
    response = await as_anon.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


async def test_get_current_user_invalid_token(as_anon: AsyncClient) -> None:
    """Test getting current user with invalid token."""
    response = await as_anon.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
