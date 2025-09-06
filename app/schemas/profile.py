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
    weight: int = Field(ge=10, le=1000)
    height: int = Field(ge=3, le=250)
    name: Optional[str] = Field(default=None, min_length=2, max_length=60)
    imageUri: HttpUrl

    @field_validator("weight", "height")
    @classmethod
    def validate_integer(cls, v):
        if isinstance(v, float) and not v.is_integer():
            raise ValueError("must be an integer")
        return int(v)

    @field_validator("imageUri")
    @classmethod
    def validate_image_uri(cls, v):
        if str(v).strip() == "":
            raise ValueError("imageUri cannot be empty")
        if not (str(v).lower().endswith(('.jpg', '.jpeg', '.png'))):
            raise ValueError("imageUri must be a URI ending with .jpg, .jpeg, or .png")
        return v
