from sqlalchemy.orm import Session
from app.schemas.activity import ActivityCreate
from app.repository import activity as activity_repo
from app.models.activity import ActivityType, Activity
from app.schemas.activity import ActivityUpdate, ActivityResponse
from typing import List, Optional
from datetime import datetime
from app.models.activity import ActivityType
from app.schemas.activity import ActivityResponse

def create_activity_usecase(db: Session, auth_id: str, activity_in: ActivityCreate):
    # Validasi activity type
    activity_type = db.query(ActivityType).filter(ActivityType.type == activity_in.activityType.value).first()
    if not activity_type:
        raise ValueError("Invalid activity type")

    # Hitung kalori
    calories_burned = activity_type.calories_per_minute * activity_in.durationInMinutes

    # Simpan ke DB lewat CRUD
    db_activity = activity_repo.create_activity(
        db=db,
        auth_id=auth_id,
        activity_type_id=activity_type.id,
        duration_minutes=activity_in.durationInMinutes,
        done_at=activity_in.doneAt,
        calories_burned=calories_burned,
    )
    return db_activity, activity_type

def delete_activity_usecase(db: Session, activity_id: int, auth_id: str) -> bool:
    return activity_repo.delete_activity(db, activity_id, auth_id)

def update_activity_usecase(db: Session, activity_id: int, auth_id: str, activity_in: ActivityUpdate):
    activity_type_id = None
    calories_burned = None

    # Cari activity lama
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.auth_id == auth_id,
        Activity.deleted_at.is_(None)
    ).first()
    if not activity:
        return None, None

    if activity_in.activityType is not None:
        activity_type = db.query(ActivityType).filter(ActivityType.type == activity_in.activityType.value).first()
        if not activity_type:
            raise ValueError("Invalid activity type")
        activity_type_id = activity_type.id
        dur = activity_in.durationInMinutes if activity_in.durationInMinutes is not None else activity.duration_in_minute
        calories_burned = activity_type.calories_per_minute * dur
    elif activity_in.durationInMinutes is not None:
        activity_type = db.query(ActivityType).filter(ActivityType.id == activity.activity_type_id).first()
        calories_burned = activity_type.calories_per_minute * activity_in.durationInMinutes

    updated_activity = activity_repo.update_activity(
        db=db,
        activity_id=activity_id,
        auth_id=auth_id,
        activity_type_id=activity_type_id,
        done_at=activity_in.doneAt,
        duration_in_minute=activity_in.durationInMinutes,
        calories_burned=calories_burned,
    )
    return updated_activity, activity_type or db.query(ActivityType).filter(ActivityType.id == updated_activity.activity_type_id).first()


def list_activities_usecase(
    db: Session,
    auth_id: str,
    limit: int = 5,
    offset: int = 0,
    activity_type: Optional[str] = None,
    done_at_from: Optional[datetime] = None,
    done_at_to: Optional[datetime] = None,
    calories_burned_min: Optional[int] = None,
    calories_burned_max: Optional[int] = None,
) -> List[ActivityResponse]:
    activities = activity_repo.list_activities(
        db=db,
        auth_id=auth_id,
        limit=limit,
        offset=offset,
        activity_type=activity_type,
        done_at_from=done_at_from,
        done_at_to=done_at_to,
        calories_burned_min=calories_burned_min,
        calories_burned_max=calories_burned_max,
    )
    result = []
    for act in activities:
        activity_type_obj = db.query(ActivityType).filter(ActivityType.id == act.activity_type_id).first()
        result.append(ActivityResponse(
            activityId=act.id,
            activityType=activity_type_obj.type if activity_type_obj else "",
            doneAt=act.done_at,
            durationInMinutes=act.duration_in_minute,
            caloriesBurned=act.calories_burned,
            createdAt=act.created_at,
            updatedAt=act.updated_at,
        ))
    return result