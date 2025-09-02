from fastapi import APIRouter
from app.api.v1.endpoints import activity

api_router = APIRouter()
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
