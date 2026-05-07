from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/acquireiq"
    google_places_api_key: str = ""
    gemini_api_key: str = ""
    hunter_api_key: str = ""

    # SMTP
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_name: str = "AcquireIQ"

    class Config:
        env_file = ".env"

settings = Settings()
