import jwt

from app.config import security_settings
from datetime import datetime, timedelta


def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(days=1),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now() + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,  # type: ignore
        key=security_settings.JWT_SECRET,
    )  # type: ignore


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None
