# app/main.py
from typing import Callable, Awaitable, cast

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.error_handlers import request_validation_exception_handler

# (opsional) inisialisasi tabel bila pakai SQLAlchemy
try:
    from app.core.database import Base, engine  # pastikan modul ini ada
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        print("Make sure your database is running and accessible.")
except Exception:
    # kalau tidak pakai DB / file tidak ada, lewati saja
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FitByte API Project for tracking fitness activities",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Registrasi global error handler (sesuai style tim)
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

# Router v1 (activity, profile, auth, file)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health():
    return {"status": "ok"}
