from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings

from fastapi import HTTPException, status, Depends
import uuid
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "iat": now})

    return jwt.encode(to_encode, settings.SECRET_KEY_JWT, algorithm=settings.ALGORITHM)


def create_refresh_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    token_id = str(uuid.uuid4())

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": token_id,  # unique id
        "exp": expire,
    }

    refresh_token = jwt.encode(
        payload, settings.SECRET_KEY_JWT, algorithm=settings.ALGORITHM
    )

    return refresh_token, token_id, expire


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY_JWT, algorithms=settings.ALGORITHM
        )
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
