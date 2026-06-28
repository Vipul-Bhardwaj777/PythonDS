from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class Address(BaseModel):
    street: str
    postal_code: str


class User(BaseModel):
    name: str
    age: int
    address: Address


user_data = {
    "name": "Vipul",
    "age": 25,
    "address": {"street": "Pharer", "postal_code": "17738djld"},
}


user = User(**user_data)

# print(user.model_dump())


class UserInfo(BaseModel):
    id: int
    user_info: List[User | Address]
    created_at: datetime

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S")}
    )


user1 = UserInfo(id=1212, user_info=[user], created_at=datetime(2026, 6, 17, 12, 48))

print(user1.model_dump_json())
