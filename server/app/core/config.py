import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fitness Tracker"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    SQLITE_DATABASE_URL: str = "sqlite+aiosqlite:///./fitness.db"

    # JWT settings
    SECRET_KEY: str = secrets.token_urlsafe(32)  # Generate a secure key if not provided
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
