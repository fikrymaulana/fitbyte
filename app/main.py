# app/main.py
from typing import Callable, Awaitable, cast
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.core.config import settings
from app.api.v1.api import api_router           # <= penting
from app.core.error_handlers import request_validation_exception_handler

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FitByte API Project for tracking fitness activities",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

HandlerType = Callable[[Request, Exception], Awaitable[JSONResponse]]
app.add_exception_handler(
    RequestValidationError, cast(HandlerType, request_validation_exception_handler)
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# >>> mount semua endpoint v1 di bawah /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health():
    return {"status": "ok"}
