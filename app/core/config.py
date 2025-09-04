from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = False
    PROJECT_NAME: str = "FitByte"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Postgres (opsional)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "fastapi_user"
    POSTGRES_PASSWORD: str = "fastapi_password"
    POSTGRES_DB: str = "fastapi_db"

    # ===== MinIO / S3 compatible =====
    MINIO_ENDPOINT: str = "localhost:9000"   # host:port (tanpa http/https)
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "uploads"
    MINIO_SECURE: bool = False               # False => http, True => https
    MINIO_REGION: str | None = None    # opsional

    # PENTING: ini bikin env yang tidak dikenal (mis. MINIO_*) diabaikan
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ---- Normalisasi agar aman kalau user menaruh http:// / spasi ----
    @field_validator("MINIO_ENDPOINT", mode="before")
    @classmethod
    def strip_scheme(cls, v: str) -> str:
        v = (v or "").strip()
        if v.startswith("http://"):
            v = v[len("http://") :]
        elif v.startswith("https://"):
            v = v[len("https://") :]
        return v

    @field_validator("MINIO_BUCKET", mode="before")
    @classmethod
    def trim_bucket(cls, v: str) -> str:
        return (v or "").strip()

settings = Settings()
