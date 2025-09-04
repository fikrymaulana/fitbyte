# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

# (opsional) kalau kamu memang pakai SQLAlchemy untuk inisialisasi tabel
try:
    from app.core.database import Base, engine  # pastikan file ini ada
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router v1 (termasuk /file yang baru kamu buat)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health():
    return {"status": "ok"}