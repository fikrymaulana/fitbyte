import secrets
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_hex(32))
    DATABASE_URL: str = "postgresql://postgres:root@localhost:5432/fitbyte"
    DEBUG: bool = False
    PROJECT_NAME: str = "FitByte"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]

    # PostgreSQL configuration fields
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "root"
    POSTGRES_DB: str = "fitbyte"

    JWT_SECRET: str = Field(default_factory=lambda: secrets.token_hex(32))
    JWT_ISS: str = "fitbyte-auth"
    JWT_AUD: str = "fitbyte-api"
    JWT_EXPIRES_SECONDS: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()
