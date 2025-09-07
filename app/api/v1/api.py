from fastapi import APIRouter, Depends
from app.api.v1.endpoints import activity, profile, auth, files
from app.api.deps import validate_content_type

api_router = APIRouter()
api_router.include_router(profile.router, prefix="", tags=["user"], dependencies=[Depends(validate_content_type)])
api_router.include_router(auth.router, dependencies=[Depends(validate_content_type)])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"], dependencies=[Depends(validate_content_type)])
api_router.include_router(files.router, prefix="", tags=["file"])
