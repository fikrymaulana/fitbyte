from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    DEBUG: bool = False
    PROJECT_NAME: str = "FitByte"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]

    # PostgreSQL configuration fields
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "fastapi_user"
    POSTGRES_PASSWORD: str = "fastapi_password"
    POSTGRES_DB: str = "fastapi_db"

    class Config:
        env_file = ".env"

settings = Settings()