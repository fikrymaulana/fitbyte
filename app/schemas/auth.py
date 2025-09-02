from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, AfterValidator
import re

Email254 = Annotated[EmailStr, Field(max_length=254)]

ALLOWED_SYMBOLS = set("!@#$")


def _password_rules(v: str) -> str:
    if len(v) < 8 or len(v) > 32:
        raise ValueError("Password length must be 8–32 characters")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one digit")
    # 'symbol' di sini = punctuation (bukan whitespace).
    if not any(ch in ALLOWED_SYMBOLS for ch in v):
        raise ValueError("Password must contain at least one symbol (e.g., !@#$)")
    return v


Password = Annotated[
    str, Field(min_length=8, max_length=32), AfterValidator(_password_rules)
]


class RegisterRequest(BaseModel):
    email: Email254
    password: Password


class RegisterResponse(BaseModel):
    email: EmailStr
    token: str


class LoginRequest(BaseModel):
    email: Email254
    password: Password


class LoginResponse(BaseModel):
    email: EmailStr
    token: str
