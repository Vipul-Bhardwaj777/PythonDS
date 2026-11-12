from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from .dependencies import AccessTokenBearer, get_refresh_token_payload

from .utils import create_access_token, create_refresh_token, verify_pass_hash
from .schemas import UserCreateResponse, UserCreate, UserLogin, UserUpdateResponse
from .service import AuthService
from app.core.config import settings
from app.core.db import get_session
import uuid

router = APIRouter()
auth_service = AuthService()


def attach_refresh_cookie(response: JSONResponse, refresh_token: str) -> JSONResponse:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRY_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )
    return response


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_signup_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):

    user_exists = await auth_service.user_exists(user_signup_data.email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists",
        )
    new_user = await auth_service.user_signup(user_signup_data, session)
    user_data = new_user.model_dump(mode="json")
    response = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Account created",
            "access_token": create_access_token(user_data),
            "user_data": user_data,
        },
    )
    return attach_refresh_cookie(response, create_refresh_token(user_data))


@router.post("/login")
async def user_login(
    login_data: UserLogin, session: AsyncSession = Depends(get_session)
):

    user = await auth_service.get_user_by_email(login_data.email, session)

    if user is not None:
        is_valid_pass = verify_pass_hash(login_data.password, user.password)

        if is_valid_pass:
            user_data = user.model_dump(mode="json")
            response = JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": create_access_token(user_data),
                    "user_data": user_data,
                }
            )
            return attach_refresh_cookie(response, create_refresh_token(user_data))

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email or Password"
    )


@router.post("/update_user")
async def update_user_account(
    uid: uuid.UUID,
    user_update_data: UserUpdateResponse,
    session: AsyncSession = Depends(get_session),
    creds=Depends(AccessTokenBearer()),
) -> UserCreateResponse:
    updated_user = await auth_service.update_user(uid, user_update_data, session)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    return updated_user


@router.get("/refresh_token")
async def refresh_token(token_data: dict = Depends(get_refresh_token_payload)):
    response = JSONResponse(
        content={
            "message": "Tokens refreshed",
            "access_token": create_access_token(token_data["user"]),
            "user": token_data["user"],
        }
    )
    return attach_refresh_cookie(response, create_refresh_token(token_data["user"]))
