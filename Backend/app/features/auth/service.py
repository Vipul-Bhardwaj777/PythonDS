from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreate, UserUpdateResponse
from .models import User
from .utils import generate_pass_hash
import uuid


class AuthService:
    async def user_signup(self, user_data: UserCreate, session: AsyncSession):
        new_user = User(**user_data.model_dump())

        new_user.password = generate_pass_hash(user_data.password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def update_user(
        self, uid: uuid.UUID, update_data: UserUpdateResponse, session: AsyncSession
    ):

        user = await session.get(User, uid)

        if user is None:
            return None

        for key, val in update_data.model_dump().items():
            setattr(user, key, val)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
