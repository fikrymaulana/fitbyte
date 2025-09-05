from fastapi import APIRouter
from app.api.v1.endpoints import activity
from app.api.v1.endpoints import profile
from app.api.v1.endpoints import auth

api_router = APIRouter()
api_router.include_router(profile.router, prefix="", tags=["user"])
api_router.include_router(auth.router)
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])