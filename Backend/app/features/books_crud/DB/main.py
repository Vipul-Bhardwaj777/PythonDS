from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# async def init_db():
#     async with engine.begin() as connection:
#         await connection.run_sync(SQLModel.metadata.create_all)


async def init_db():
    """No schema creation here; Alembic manages migrations."""
    pass


async def get_session():

    async with async_session() as session:
        yield session
