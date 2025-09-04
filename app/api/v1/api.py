from fastapi import APIRouter
from app.api.v1.endpoints import auth, activity

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])