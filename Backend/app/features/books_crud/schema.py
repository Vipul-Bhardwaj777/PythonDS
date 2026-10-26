from pydantic import BaseModel
from datetime import datetime, date
import uuid


class BookResponse(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    price: float
    publisher: str
    publish_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    publisher: str
    publish_date: date
    page_count: int
    language: str


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = None
    publisher: str | None = None
