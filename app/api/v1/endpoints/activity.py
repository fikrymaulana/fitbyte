from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.activity import ActivityCreate, ActivityResponse
from app.api.deps import get_db
from fastapi.security import OAuth2PasswordBearer
from app.usecase.activity import create_activity_usecase

router = APIRouter() 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy function, ganti dengan logic verifikasi JWT Anda
def get_current_user_id(token: str = Depends(oauth2_scheme)):
    # Implementasi asli: decode JWT, ambil user_id/auth_id
    # Contoh dummy:
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return "dummy-auth-id"  # Ganti dengan hasil decode JWT

@router.post("/", response_model=ActivityResponse, status_code=201)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    auth_id: str = "1",
):
    try:
        db_activity, activity_type = create_activity_usecase(db, auth_id, activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("ERROR:", e)  # Tambahkan ini untuk debug
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