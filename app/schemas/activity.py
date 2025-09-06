from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum
from typing import Optional

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

    @field_validator("doneAt")
    @classmethod
    def validate_done_at(cls, v):
        # Ensure it's a valid datetime 
        if not isinstance(v, datetime):
            raise ValueError("doneAt must be a valid datetime")
        return v

    @field_validator("durationInMinutes")
    @classmethod
    def validate_integer(cls, v):
        if isinstance(v, float) and not v.is_integer():
            raise ValueError("must be an integer")
        return int(v)

class ActivityResponse(BaseModel):
    activityId: int
    activityType: str
    doneAt: datetime
    durationInMinutes: int
    caloriesBurned: int
    createdAt: datetime
    updatedAt: datetime
    
from typing import Optional

class ActivityUpdate(BaseModel):
    activityType: Optional[ActivityTypeEnum] = Field(None, description="Activity type name")
    doneAt: Optional[datetime] = None
    durationInMinutes: Optional[int] = Field(None, ge=1, le=1440)