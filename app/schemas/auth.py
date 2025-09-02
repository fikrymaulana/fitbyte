from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)


class RegisterResponse(BaseModel):
    email: EmailStr
    token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)


class LoginResponse(BaseModel):
    email: EmailStr
    token: str
