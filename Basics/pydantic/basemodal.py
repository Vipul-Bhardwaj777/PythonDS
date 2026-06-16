from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool

input_data = {'id': 101, 'name': 'ChaiCode', 'is_active': True}

user1 = User(**input_data)

print(user1)