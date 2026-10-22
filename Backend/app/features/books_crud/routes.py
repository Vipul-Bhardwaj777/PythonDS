from fastapi import APIRouter, HTTPException, status
from app.features.books_crud.schema import BookModel, UpdateBookModel
from app.features.books_crud.DB.data_base import books

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/")
async def get_all_books() -> list[BookModel]:
    return books


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookModel) -> BookModel:
    new_book = book_data.model_dump()
    books.append(new_book)

    return new_book


@router.get("/{book_id}")
async def get_book(book_id: int) -> BookModel:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")


@router.patch("/{book_id}")
async def update_book(book_id: int, update_data: UpdateBookModel) -> BookModel:
    for book in books:
        if book["id"] == book_id:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                book[key] = value

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")
