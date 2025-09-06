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

    @field_validator("doneAt", mode="before")
    @classmethod
    def validate_done_at(cls, v):
        # Check for None
        if v is None:
            raise ValueError("doneAt is required")

        # If doneAt is string, check if it's in correct datetime format
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("invalid")
        else:
            raise ValueError("invalid")
        return v

    @field_validator("durationInMinutes", mode="before")
    @classmethod
    def validate_integer(cls, v):
        if isinstance(v, bool):
            raise ValueError("durationInMinutes must be a number, not a boolean")
        if not isinstance(v, (int, float)):
            raise ValueError("durationInMinutes must be a number")
        if isinstance(v, float) and not v.is_integer():
            raise ValueError("durationInMinutes must be an integer")
        return int(v)

class ActivityResponse(BaseModel):
    activityId: str
    activityType: str
    doneAt: str
    durationInMinutes: int
    caloriesBurned: int
    createdAt: datetime
    updatedAt: datetime
    
from typing import Optional

class ActivityUpdate(BaseModel):
    activityType: ActivityTypeEnum = Field(..., description="Activity type name")
    doneAt: datetime
    durationInMinutes: int = Field(..., ge=1, le=1440)

    @field_validator("doneAt", mode="before")
    @classmethod
    def validate_done_at(cls, v):
        # If doneAt is string, check if it's in correct datetime format
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("invalid date time format")
        elif isinstance(v, datetime):
            return v
        else:
            raise ValueError("invalid")
        return v

    @field_validator("durationInMinutes", mode="before")
    @classmethod
    def validate_integer(cls, v):
        if isinstance(v, bool):
            raise ValueError("durationInMinutes must be a number, not a boolean")
        if not isinstance(v, (int, float)):
            raise ValueError("durationInMinutes must be a number")
        if isinstance(v, float) and not v.is_integer():
            raise ValueError("durationInMinutes must be an integer")
        return int(v)