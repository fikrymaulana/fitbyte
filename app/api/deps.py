from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt

from app.core.database import get_db
from app.core.config import settings
from app.core.security import decode_access_token
from app.models.auth import Authentication

# Skema ini sudah Anda definisikan, dan akan kita gunakan.
bearer = HTTPBearer(auto_error=True)


def get_current_claims(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    token = creds.credentials
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
            audience=settings.JWT_AUD,
            issuer=settings.JWT_ISS,
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def _get_token_from_header(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


# ── FUNGSI INI TIDAK DIUBAH ─────────────────────────────────
def get_current_user_payload(
    authorization: Optional[str] = Header(None),
) -> Dict[str, Any]:
    token = _get_token_from_header(authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if not payload.get("sub") or not payload.get("email"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# ── HANYA FUNGSI INI YANG KITA PERBAIKI ───────────────
def get_current_user(
    # PERUBAHAN UTAMA: Ganti 'Header(None)' dengan 'Depends(bearer)'
    # Ini akan menghubungkannya langsung ke tombol "Authorize" global.
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> Authentication:
    # Kita sekarang mendapatkan token langsung dari 'creds', lebih andal.
    token = creds.credentials
    
    # Sisa logika di bawah ini sudah benar dan tidak diubah.
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = (
        db.query(Authentication)
        .filter(Authentication.id == user_id, Authentication.deleted_at.is_(None))
        .one_or_none()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user