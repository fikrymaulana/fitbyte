from typing import Callable, Awaitable, cast

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from starlette.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models import auth
from app.core.error_handlers import request_validation_exception_handler

# Create database tables (with error handling)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")
    print("Make sure PostgreSQL is running and accessible.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FitByte API Project for tracking fitness activities",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Supress Pyright's complaint
HandlerType = Callable[[Request, Exception], Awaitable[JSONResponse]]
app.add_exception_handler(
    RequestValidationError, cast(HandlerType, request_validation_exception_handler)
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health():
    return {"status": "ok"}
