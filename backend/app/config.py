from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/acquireiq"
    redis_url: str = "redis://localhost:6379/0"
    google_places_api_key: str = ""
    gemini_api_key: str = ""
    opencorporates_api_token: str = ""
    hunter_api_key: str = ""
    secret_key: str = "change-me-in-production"

    class Config:
        env_file = ".env"

settings = Settings()
