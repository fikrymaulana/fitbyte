from sqlalchemy.orm import Session
from app.models.activity import Activity
from datetime import datetime

def create_activity(db: Session, auth_id: str, activity_type_id: int, duration_minutes: int, done_at: datetime, calories_burned: int = None) -> Activity:
    db_activity = Activity(
        auth_id=auth_id,
        activity_type_id=activity_type_id,
        duration_in_minute=duration_minutes,
        calories_burned=calories_burned,
        done_at = done_at,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity