from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import desc, select
from .schema import BookCreate, BookUpdate
from .DB.models import Book
import uuid


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def create_book(self, book_data: BookCreate, session: AsyncSession):
        new_book = Book(**book_data.model_dump())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        return await session.get(Book, book_uid)

    async def update_book(
        self, book_uid: uuid.UUID, update_data: BookUpdate, session: AsyncSession
    ):
        book = await session.get(Book, book_uid)

        if book is None:
            return None
        for key, val in update_data.model_dump(exclude_unset=True).items():
            setattr(book, key, val)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        book = await session.get(Book, book_uid)

        if book is None:
            return None
        await session.delete(book)
        await session.commit()
        return book
