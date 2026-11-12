from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db import get_session
from .service import BookService
from .schema import BookCreate, BookResponse, BookUpdate
import uuid
from app.features.auth.dependencies import AccessTokenBearer

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()


@router.get("/")
async def get_all_books(
    session: AsyncSession = Depends(get_session), creds=Depends(access_token_bearer)
) -> list[BookResponse]:
    print(creds, "creds")
    return await book_service.get_all_books(session)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(get_session),
    creds=Depends(access_token_bearer),
) -> BookResponse:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@router.get("/{book_uid}")
async def get_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    creds=Depends(access_token_bearer),
) -> BookResponse:
    book = await book_service.get_book(book_uid, session)

    if book is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")


@router.patch("/{book_uid}")
async def update_book(
    book_uid: uuid.UUID,
    update_data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    creds=Depends(access_token_bearer),
) -> BookResponse:
    book = await book_service.update_book(book_uid, update_data, session)

    if book is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")


@router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    creds=Depends(access_token_bearer),
):
    book = await book_service.delete_book(book_uid, session)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
        )
