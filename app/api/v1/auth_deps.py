# app/api/v1/auth_deps.py
from typing import Any, Dict
from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from app.core.config import settings

ALGORITHM = "HS256"  # samakan dengan issuer token kamu

def _jwt_from_header(authorization: str | None = Header(None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return authorization.split(" ", 1)[1].strip()

def get_current_user(token: str = Depends(_jwt_from_header)) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload: missing 'sub'")

    return {"sub": str(sub), "claims": payload}
