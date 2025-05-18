import asyncio
from collections.abc import AsyncGenerator, Generator
from datetime import UTC, datetime

import pytest
from app.core.security import create_access_token, get_password_hash
from app.db.session import get_db
from app.main import app
from app.models.base import Base
from app.models.models import Exercise, MuscleGroup, User
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_app() -> FastAPI:
    """Create a fresh database for each test session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Override the get_db dependency
    async def override_get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            finally:
                await session.rollback()
                await session.close()

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession]:
    """Create a fresh database session for each test."""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            # Rollback any pending changes
            await session.rollback()
            # Delete all data from all tables
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
            await session.commit()
            await session.close()


@pytest.fixture
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient]:
    """Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test", follow_redirects=True) as ac:
        yield ac


@pytest.fixture
async def muscle_group(db_session: AsyncSession) -> MuscleGroup:
    """Create a test muscle group."""
    muscle_group = MuscleGroup(name="Test Muscle Group")
    db_session.add(muscle_group)
    await db_session.commit()
    await db_session.refresh(muscle_group)
    return muscle_group


@pytest.fixture
async def exercise(db_session: AsyncSession, muscle_group: MuscleGroup) -> Exercise:
    """Create a test exercise."""
    exercise = Exercise(
        name="Test Exercise",
        description="Test exercise description",
        muscle_group=muscle_group,
        aliases=["test alias", "another alias"],
    )
    db_session.add(exercise)
    await db_session.commit()
    await db_session.refresh(exercise)
    return exercise


@pytest.fixture
async def user(db_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword123"),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def as_anon(client: AsyncClient) -> AsyncClient:
    """Return a client without authentication headers."""
    return client


@pytest.fixture
async def as_user(client: AsyncClient, user: User) -> AsyncClient:
    """Return a client with authentication headers for the test user."""
    token = create_access_token(subject=user.id)
    client.headers["Authorization"] = f"Bearer {token}"
    return client
