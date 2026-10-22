from pydantic import BaseModel
from datetime import date


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    price: float
    publisher: str
    publish_date: date
    page_count: int
    language: str


class UpdateBookModel(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = None
    publisher: str | None = None
