from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate, ActivityTypeEnum
from app.api.deps import get_db, get_current_user_payload
from app.usecase.activity import create_activity_usecase, delete_activity_usecase, update_activity_usecase, list_activities_usecase
from typing import List, Optional
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



router = APIRouter()

@router.post("/", response_model=ActivityResponse, status_code=201)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    auth_id = payload["sub"]
    try:
        db_activity, activity_type = create_activity_usecase(db, auth_id, activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    return ActivityResponse(
        activityId=db_activity.id,
        activityType=activity_type.type,
        doneAt=db_activity.done_at,
        durationInMinutes=db_activity.duration_in_minute,
        caloriesBurned=db_activity.calories_burned,
        createdAt=db_activity.created_at,
        updatedAt=db_activity.updated_at,
    )
    
@router.delete("/{activityId}", status_code=200)
def delete_activity(
    activityId: int = Path(..., description="ID aktivitas"),
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    auth_id = payload["sub"]
    try:
       deleted = delete_activity_usecase(db, activityId, auth_id)
       if not deleted:
            raise HTTPException(status_code=404, detail="Activity not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Activity deleted successfully"}

from app.schemas.activity import ActivityUpdate

@router.patch("/{activityId}", response_model=ActivityResponse, status_code=200)
def update_activity(
    activityId: int = Path(..., description="ID aktivitas"),
    activity: ActivityUpdate = None,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    auth_id = payload["sub"]
    try:
        updated_activity, activity_type = update_activity_usecase(db, activityId, auth_id, activity)
        if not updated_activity:
            raise HTTPException(status_code=404, detail="Activity not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    return ActivityResponse(
        activityId=updated_activity.id,
        activityType=activity_type.type,
        doneAt=updated_activity.done_at,
        durationInMinutes=updated_activity.duration_in_minute,
        caloriesBurned=updated_activity.calories_burned,
        createdAt=updated_activity.created_at,
        updatedAt=updated_activity.updated_at,
    )
    
@router.get("/", response_model=List[ActivityResponse], status_code=200)
def list_activities(
    db: Session = Depends(get_db),
    limit: int = 5,
    offset: int = 0,
    activityType: Optional[ActivityTypeEnum] = None,
    doneAtFrom: Optional[datetime] = None,
    doneAtTo: Optional[datetime] = None,
    caloriesBurnedMin: Optional[int] = None,
    caloriesBurnedMax: Optional[int] = None,
    payload: dict = Depends(get_current_user_payload),
):
    auth_id = payload["sub"]
    try:
        result = list_activities_usecase(
            db=db,
            auth_id=auth_id,
            limit=limit,
            offset=offset,
            activity_type=activityType.value if activityType else None,
            done_at_from=doneAtFrom,
            done_at_to=doneAtTo,
            calories_burned_min=caloriesBurnedMin,
            calories_burned_max=caloriesBurnedMax,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")