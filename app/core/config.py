# app/core/config.py
from typing import Optional
import secrets
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_hex(32))
    DEBUG: bool = False
    PROJECT_NAME: str = "FitByte"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # === PostgreSQL (aktif) ===
    # Langsung pakai DATABASE_URL; kalau kosong, dibangun dari komponen di bawah.
    DATABASE_URL: Optional[str] = None
    POSTGRES_SERVER: str = "localhost"      # ganti ke 'db' kalau pakai docker service name
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "root"
    POSTGRES_DB: str = "fitbyte"

    # JWT (punya tim)
    JWT_SECRET: str = Field(default_factory=lambda: secrets.token_hex(32))
    JWT_ISS: str = "fitbyte-auth"
    JWT_AUD: str = "fitbyte-api"
    JWT_EXPIRES_SECONDS: int = 3600

    # === MinIO (tetap dipakai) ===
    MINIO_ENDPOINT: Optional[str] = None     # contoh: "minio:9000" (tanpa http/https)
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    MINIO_BUCKET: Optional[str] = "files"
    MINIO_SECURE: bool = False               # http=False, https=True
    MINIO_REGION: Optional[str] = None

    # Pydantic v2 config (.env)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ---- Normalisasi/auto-build DATABASE_URL kalau belum diset ----
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def build_db_url(cls, v, info):
        if v and str(v).strip():
            return v
        data = info.data
        return (
            f"postgresql://{data.get('POSTGRES_USER')}:{data.get('POSTGRES_PASSWORD')}"
            f"@{data.get('POSTGRES_SERVER')}:{data.get('POSTGRES_PORT')}/{data.get('POSTGRES_DB')}"
        )

settings = Settings()
