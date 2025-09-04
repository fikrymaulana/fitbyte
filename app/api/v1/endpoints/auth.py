from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.auth import Authentication
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)
from app.api.deps import get_current_user, get_current_user_payload

from cuid2 import cuid_wrapper

generate_cuid = cuid_wrapper()

router = APIRouter(tags=["Auth"])


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    # cek email
    q = db.execute(select(Authentication).where(Authentication.email == payload.email))
    existing = q.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    hashed = get_password_hash(payload.password)

    new_id = generate_cuid()

    user = Authentication(id=new_id, email=payload.email, password_hash=hashed)

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(sub=user.id, email=user.email)
    return RegisterResponse(email=user.email, token=token)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    q = db.execute(select(Authentication).where(Authentication.email == payload.email))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(sub=user.id, email=user.email)
    return LoginResponse(email=user.email, token=token)


# High-throughput read-only route → stateless
@router.get("/me-lite")
def me_lite(payload=Depends(get_current_user_payload)):
    return {"sub": payload["sub"], "email": payload["email"]}


# Sensitive route → stateful
@router.get("/me")
def me(current_user: Authentication = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
