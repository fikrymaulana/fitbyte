from fastapi import APIRouter
from app.api.v1.endpoints import activity, profile, auth, file

api_router = APIRouter()

# router milik tim
api_router.include_router(profile.router, prefix="", tags=["user"])
api_router.include_router(auth.router)
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(file.router, tags=["file"])
