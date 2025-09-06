from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.profile import Profile
from app.models.auth import Authentication
from app.schemas.profile import ProfileOut, ProfilePatch

router = APIRouter()
bearer = HTTPBearer(auto_error=False)

def current_profile(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> Profile:
    if not creds or not creds.scheme.lower().startswith("bearer"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")

    try:
        payload = decode_access_token(creds.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token")

    auth_id = payload.get("sub")

    if not auth_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token payload")

    user = db.query(Profile).filter(Profile.auth_id == auth_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token subject")
    
    return user

@router.get("/user", response_model=ProfileOut, status_code=200)
def get_user(
    db: Session = Depends(get_db),
    me: Profile = Depends(current_profile),
):
    # ambil authentication berdasarkan auth_id dari profile
    auth = db.query(Authentication).filter(Authentication.id == me.auth_id).first()
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication not found")
    
    return ProfileOut(
        preference=me.preference,
        weightUnit=me.weight_unit,
        heightUnit=me.height_unit,
        weight=float(me.weight) if me.weight is not None else None,
        height=float(me.height) if me.height is not None else None,
        email=auth.email,
        name=me.name,
        imageUri=me.image_uri,
    )

@router.patch("/user", response_model=dict, status_code=200)  # response body plain object sesuai kontrak
def patch_user(
    payload: ProfilePatch,
    db: Session = Depends(get_db),
    me: Profile = Depends(current_profile),
):
    me.preference = payload.preference
    me.weight_unit = payload.weightUnit
    me.height_unit = payload.heightUnit
    me.weight = payload.weight
    me.height = payload.height
    me.name = payload.name
    me.image_uri = str(payload.imageUri) if payload.imageUri else None

    db.add(me)
    db.commit()
    db.refresh(me)

    return {
        "preference": me.preference,
        "weightUnit": me.weight_unit,
        "heightUnit": me.height_unit,
        "weight": me.weight if me.weight is not None else None,
        "height": me.height if me.height is not None else None,
        "name": me.name,
        "imageUri": me.image_uri,
    }
