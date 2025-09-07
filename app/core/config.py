from typing import List, Optional, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    # ===== Base (sesuai versi tim) =====
    SECRET_KEY: str
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = False
    PROJECT_NAME: str = "FitByte"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # ===== Postgres (opsional) =====
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "fastapi_user"
    POSTGRES_PASSWORD: str = "fastapi_password"
    POSTGRES_DB: str = "fastapi_db"

    # ===== MinIO (opsional, aman kalau .env tidak ada) =====
    # gunakan Optional agar tidak wajib diisi ketika env tim belum siap
    MINIO_ENDPOINT: Optional[str] = None     # contoh: "minio:9000" (tanpa http/https)
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    MINIO_BUCKET: Optional[str] = "files"
    MINIO_SECURE: bool = False               # False => http, True => https
    MINIO_REGION: Optional[str] = None

    # Abaikan env yang tidak dikenal (mis. MINIO_* lain)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ---- Normalisasi agar aman bila user salah input (http:// / spasi) ----
    @field_validator("MINIO_ENDPOINT", mode="before")
    @classmethod
    def _strip_scheme(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        s = str(v).strip()
        if s.startswith("http://"):
            s = s[len("http://") :]
        elif s.startswith("https://"):
            s = s[len("https://") :]
        return s or None

    @field_validator("MINIO_BUCKET", mode="before")
    @classmethod
    def _trim_bucket(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        s = str(v).strip()
        return s or None


settings = Settings()
