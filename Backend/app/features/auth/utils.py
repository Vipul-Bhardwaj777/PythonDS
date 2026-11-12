from datetime import datetime, timedelta, timezone
import logging
from passlib.context import CryptContext
import jwt
from app.core.config import settings
import uuid

passw_context = CryptContext(schemes=["bcrypt"])


def generate_pass_hash(password: str) -> str:
    return passw_context.hash(password)


def verify_pass_hash(password: str, hash: str) -> bool:
    return passw_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now(timezone.utc) + (
        expiry
        if expiry is not None
        else timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRY_SECONDS)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token


def create_refresh_token(user_data: dict) -> str:
    return create_access_token(
        user_data,
        expiry=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRY_DAYS),
        refresh=True,
    )


def decode_token(token: str) -> dict:

    try:
        token_data = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        return token_data

    except jwt.PyJWTError:
        logging.exception("Failed to decode token")
        raise
