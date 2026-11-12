from fastapi import HTTPException, Request, status
from fastapi.requests import HTTPConnection
from fastapi.security import HTTPBearer
import jwt

from .utils import decode_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: HTTPConnection) -> dict | None:
        creds = await super().__call__(request)

        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )

        return self.validate(creds.credentials)

    def validate(self, token: str) -> dict:
        token_data = self.verify_token(token)
        self.verify_token_data(token_data)
        return token_data

    def verify_token(self, token: str) -> dict:
        try:
            return decode_token(token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired"
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data):
        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide valid access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data):
        if not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide valid refresh token",
            )


async def get_refresh_token_payload(request: Request) -> dict:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return RefreshTokenBearer().validate(refresh_token)
