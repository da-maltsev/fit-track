from datetime import UTC, datetime

from app.core.security import get_password_hash
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
        hashed_password=get_password_hash("testpassword123"),
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


async def test_login_success(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test successful login through the API."""
    # First create a user
    user = User(
        email="login_test@example.com",
        username="logintestuser",
        hashed_password=get_password_hash("testpassword123"),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Try to login
    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": "login_test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test login with wrong password through the API."""
    # First create a user
    user = User(
        email="wrong_pass@example.com",
        username="wrongpassuser",
        hashed_password=get_password_hash("testpassword123"),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Try to login with wrong password
    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": "wrong_pass@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


async def test_login_nonexistent_user(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test login with nonexistent user through the API."""
    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": "nonexistent@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


async def test_get_current_user(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test getting current user information through the API."""
    # First create a user
    user = User(
        email="me_test@example.com",
        username="metestuser",
        hashed_password=get_password_hash("testpassword123"),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Login to get token
    login_response = await client.post(
        "/api/v1/users/login",
        json={
            "email": "me_test@example.com",
            "password": "testpassword123",
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Get current user info
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me_test@example.com"
    assert data["username"] == "metestuser"
    assert data["id"] == user.id


async def test_get_current_user_no_token(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test getting current user without token."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


async def test_get_current_user_invalid_token(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test getting current user with invalid token."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
