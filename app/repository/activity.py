from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.activity import Activity, ActivityType


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

from datetime import datetime

def delete_activity(db: Session, activity_id: int, auth_id: str) -> bool:
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.auth_id == auth_id,
        Activity.deleted_at.is_(None) 
    ).first()
    if not activity:
        return False
    activity.deleted_at = datetime.utcnow()
    db.commit()
    return True

def update_activity(
    db: Session,
    activity_id: int,
    auth_id: str,
    activity_type_id: int = None,
    done_at: datetime = None,
    duration_in_minute: int = None,
    calories_burned: int = None,
) -> Activity:
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.auth_id == auth_id,
        Activity.deleted_at.is_(None)
    ).first()
    if not activity:
        return None
    if activity_type_id is not None:
        activity.activity_type_id = activity_type_id
    if done_at is not None:
        activity.done_at = done_at
    if duration_in_minute is not None:
        activity.duration_in_minute = duration_in_minute
    if calories_burned is not None:
        activity.calories_burned = calories_burned
    activity.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(activity)
    return activity

def list_activities(
    db: Session,
    auth_id: str,
    limit: int = 5,
    offset: int = 0,
    activity_type: Optional[str] = None,
    done_at_from: Optional[datetime] = None,
    done_at_to: Optional[datetime] = None,
    calories_burned_min: Optional[int] = None,
    calories_burned_max: Optional[int] = None,
) -> List[Activity]:
    query = db.query(Activity).filter(
        Activity.auth_id == auth_id,
        Activity.deleted_at.is_(None)
    )
    if activity_type:
        query = query.join(ActivityType).filter(ActivityType.type == activity_type)
    if done_at_from:
        query = query.filter(Activity.done_at >= done_at_from)
    if done_at_to:
        query = query.filter(Activity.done_at <= done_at_to)
    if calories_burned_min is not None:
        query = query.filter(Activity.calories_burned >= calories_burned_min)
    if calories_burned_max is not None:
        query = query.filter(Activity.calories_burned <= calories_burned_max)
    return query.order_by(Activity.done_at.desc()).offset(offset).limit(limit).all()