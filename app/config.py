from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Documents API"
    app_description: str = "Service for versioned file storage and AI analysis"
    app_version: str = "0.1.0"

    database_url: str
    storage_path: str = "./storage"
    openai_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
