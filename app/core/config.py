# app/core/config.py
import secrets
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_hex(32))
    DEBUG: bool = False
    PROJECT_NAME: str = "FitByte"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # === PostgreSQL (pakai DATABASE_URL langsung) ===
    # Contoh format (SQLAlchemy): postgresql+psycopg2://user:pass@host:5432/dbname
    DATABASE_URL: str

    # JWT (hanya “placeholder” – auth module tim yang akan pakai)
    JWT_SECRET: str = Field(default_factory=lambda: secrets.token_hex(32))
    JWT_ISS: str = "fitbyte-auth"
    JWT_AUD: str = "fitbyte-api"
    JWT_EXPIRES_SECONDS: int = 3600

    # MinIO configuration
    MINIO_ENDPOINT: str = "localhost"
    MINIO_PORT: int = 9000
    MINIO_ACCESS_KEY: str = "jmiLvxklmDtGadZ8dabO"
    MINIO_SECRET_KEY: str = "KlAEFY5jH094lRsAHKoddrL8cfEMfwGmrJzGs8lB"
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str = "fitbyte"

    class Config:
        env_file = ".env"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
