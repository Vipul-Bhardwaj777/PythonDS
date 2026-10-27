from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateResponse, UserCreate, UserUpdateResponse
from .service import AuthService
from app.features.books_crud.DB.main import get_session
import uuid

router = APIRouter()
auth_service = AuthService()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_signup_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserCreateResponse:

    user_exists = await auth_service.user_exists(user_signup_data.email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists",
        )
    new_user = await auth_service.user_signup(user_signup_data, session)
    return new_user


@router.post("/update_user")
async def update_user_account(
    uid: uuid.UUID,
    user_update_data: UserUpdateResponse,
    session: AsyncSession = Depends(get_session),
) -> UserCreateResponse:
    updated_user = await auth_service.update_user(uid, user_update_data, session)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    return updated_user
