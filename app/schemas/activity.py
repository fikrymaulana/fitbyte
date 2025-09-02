from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ActivityTypeEnum(str, Enum):
    walking = "Walking"
    yoga = "Yoga"
    stretching = "Stretching"
    cycling = "Cycling"
    swimming = "Swimming"
    dancing = "Dancing"
    hiking = "Hiking"
    running = "Running"
    hiit = "HIIT"
    jumprope = "JumpRope"

class ActivityCreate(BaseModel):
    activityType: ActivityTypeEnum = Field(..., description="Activity type name")
    doneAt: datetime
    durationInMinutes: int = Field(..., ge=1, le=1440)

class ActivityResponse(BaseModel):
    activityId: int
    activityType: str
    doneAt: datetime
    durationInMinutes: int
    caloriesBurned: int
    createdAt: datetime
    updatedAt: datetime