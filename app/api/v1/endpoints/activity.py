from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate, ActivityTypeEnum
from app.api.deps import get_db
from app.usecase.activity import create_activity_usecase, delete_activity_usecase, update_activity_usecase, list_activities_usecase
from typing import List, Optional
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token

router = APIRouter()
bearer = HTTPBearer(auto_error=False)

def current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> str:
    if not creds or not creds.scheme.lower().startswith("bearer"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")

    try:
        payload = decode_access_token(creds.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token")

    auth_id = payload.get("sub")

    if not auth_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token payload")
    
    return auth_id

@router.post("", response_model=ActivityResponse, status_code=201)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    authId: str = Depends(current_user),
):
    try:
        db_activity, activity_type = create_activity_usecase(db, authId, activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    done_at_str = db_activity.done_at.isoformat().replace('+00:00', 'Z').replace('000Z', 'Z').replace('00Z', 'Z').replace('0Z', 'Z')
    return ActivityResponse(
        activityId=str(db_activity.id),
        activityType=activity_type.type,
        doneAt=done_at_str,
        durationInMinutes=db_activity.duration_in_minute,
        caloriesBurned=db_activity.calories_burned,
        createdAt=db_activity.created_at,
        updatedAt=db_activity.updated_at,
    )

@router.delete("", status_code=404)
def patch_activity_missing_id():
    raise HTTPException(status_code=404, detail="Activity ID is required")

@router.delete("/{activityId}", status_code=200)
def delete_activity(
    activityId: str = Path(..., description="ID aktivitas"),
    db: Session = Depends(get_db),
    authId: str = Depends(current_user),
):
    try:
        activity_id_int = int(activityId)
    except ValueError:
        raise HTTPException(status_code=404, detail="Activity not found")
    try:
       deleted = delete_activity_usecase(db, activity_id_int, authId)
       if not deleted:
            raise HTTPException(status_code=404, detail="Activity not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Activity deleted successfully"}


@router.patch("", status_code=404)
def patch_activity_missing_id():
    raise HTTPException(status_code=404, detail="Activity ID is required")

@router.patch("/{activityId}", response_model=ActivityResponse, status_code=200)
def update_activity(
    activityId: str = Path(..., description="ID aktivitas"),
    activity: ActivityUpdate = None,
    db: Session = Depends(get_db),
    authId: str = Depends(current_user),
):
    try:
        activity_id_int = int(activityId)
    except ValueError:
        raise HTTPException(status_code=404, detail="Activity not found")
    try:
        updated_activity, activity_type = update_activity_usecase(db, activity_id_int, authId, activity)
        if not updated_activity:
            raise HTTPException(status_code=404, detail="Activity not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    done_at_str = updated_activity.done_at.isoformat().replace('+00:00', 'Z').replace('000Z', 'Z').replace('00Z', 'Z').replace('0Z', 'Z')
    return ActivityResponse(
        activityId=str(updated_activity.id),
        activityType=activity_type.type,
        doneAt=done_at_str,
        durationInMinutes=updated_activity.duration_in_minute,
        caloriesBurned=updated_activity.calories_burned,
        createdAt=updated_activity.created_at,
        updatedAt=updated_activity.updated_at,
    )
    
@router.get("", response_model=List[ActivityResponse], status_code=200)
def list_activities(
    db: Session = Depends(get_db),
    limit: int = 5,
    offset: int = 0,
    activityType: Optional[ActivityTypeEnum] = None,
    doneAtFrom: Optional[datetime] = None,
    doneAtTo: Optional[datetime] = None,
    caloriesBurnedMin: Optional[int] = None,
    caloriesBurnedMax: Optional[int] = None,
    authId: str = Depends(current_user),
):
    try:
        result = list_activities_usecase(
            db=db,
            auth_id=authId,
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