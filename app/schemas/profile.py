from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator, HttpUrl

Preference = Literal["CARDIO", "WEIGHT"]
WeightUnit = Literal["KG", "LBS"]
HeightUnit = Literal["CM", "INCH"]

class ProfileOut(BaseModel):
    preference: Optional[Preference] = None
    weightUnit: Optional[WeightUnit] = None
    heightUnit: Optional[HeightUnit] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    email: EmailStr
    name: Optional[str] = None
    imageUri: Optional[HttpUrl] = None

class ProfilePatch(BaseModel):
    preference: Preference
    weightUnit: WeightUnit
    heightUnit: HeightUnit
    weight: float = Field(ge=10, le=1000)
    height: float = Field(ge=3, le=250)
    name: Optional[str] = Field(default=None, min_length=2, max_length=60)
    imageUri: Optional[HttpUrl] = None

    @field_validator("weight", "height")
    @classmethod
    def to_float(cls, v):
        # ensure JSON numbers are float (SQLAlchemy Numeric is fine receiving Decimal, but we keep float here)
        return float(v)
