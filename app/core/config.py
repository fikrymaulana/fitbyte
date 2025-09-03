from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = False
    PROJECT_NAME: str = "FitByte"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Postgres (opsional)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "fastapi_user"
    POSTGRES_PASSWORD: str = "fastapi_password"
    POSTGRES_DB: str = "fastapi_db"

    # --- MinIO opsional ---
    MINIO_ENDPOINT: Optional[str] = None    # contoh: "minio:9000"
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    MINIO_BUCKET: Optional[str] = "files"
    MINIO_SECURE: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
