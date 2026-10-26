from pydantic import BaseModel


class TodoReq(BaseModel):
    title: str
    description: str


class TodoRes(BaseModel):
    message: str
