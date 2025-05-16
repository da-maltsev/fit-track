from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fitness Tracker"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    SQLITE_DATABASE_URL: str = "sqlite+aiosqlite:///./fitness.db"
    
    class Config:
        case_sensitive = True

settings = Settings() 