from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    password: str = Field(min_length=6)


class UserCreateResponse(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    password: str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateResponse(BaseModel):
    username: str
    first_name: str
    last_name: str
