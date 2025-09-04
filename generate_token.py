# generate_token.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings  # pakai SECRET_KEY dari .env

ALGORITHM = "HS256"  # samakan dengan decoder kamu

def create_test_token(subject: str = "test-user", minutes: int = 30) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=minutes)
    payload = {
        "sub": subject,                # ganti sesuai kebutuhan (user_id/email)
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

if __name__ == "__main__":
    print(create_test_token())
