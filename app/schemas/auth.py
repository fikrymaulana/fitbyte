from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, AfterValidator, BeforeValidator
import re

from app.core.sanitize import sanitize_email_input

ALLOWED_SYMBOLS = set("!@#$")


def _password_rules(v: str) -> str:
    if len(v) < 8 or len(v) > 32:
        raise ValueError("Password length must be 8–32 characters")
    # TODO: Re-enable full requirement later after testing
    # if any(ch.isspace() for ch in v):
    #     raise ValueError("Password must not contain whitespace")
    # if not re.search(r"[a-z]", v):
    #     raise ValueError("Password must contain at least one lowercase letter")
    # if not re.search(r"[A-Z]", v):
    #     raise ValueError("Password must contain at least one uppercase letter")
    # if not re.search(r"\d", v):
    #     raise ValueError("Password must contain at least one digit")
    # if not any(ch in ALLOWED_SYMBOLS for ch in v):
    #     raise ValueError("Password must contain at least one symbol (e.g., !@#$)")
    return v


EmailSanitized = Annotated[
    EmailStr, BeforeValidator(sanitize_email_input), Field(max_length=254)
]
Password = Annotated[
    str, Field(min_length=8, max_length=32), AfterValidator(_password_rules)
]


class RegisterRequest(BaseModel):
    email: EmailSanitized
    password: Password


class RegisterResponse(BaseModel):
    email: EmailStr
    token: str


class LoginRequest(BaseModel):
    email: EmailSanitized
    password: Password


class LoginResponse(BaseModel):
    email: EmailStr
    token: str
