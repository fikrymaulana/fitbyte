from sqlalchemy.orm import Session
from app.schemas.activity import ActivityCreate
from app.repository import activity as activity_repo  # gunakan alias agar jelas
from app.models.activity import ActivityType

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