from fastapi import APIRouter, Header
from typing import Optional
from app.features.first_rest.schema import TodoReq, TodoRes


router = APIRouter()


@router.get("/greet/{state}")
async def greet(city: str, state: str, name: Optional[str] = "User") -> dict:
    return {"message": f"Hii {name} from {city}, {state}!"}


@router.post("/create_todo", response_model=TodoRes)
async def create_todo(data: TodoReq) -> TodoRes:
    return {"message": "Todo created!"}


@router.get("/get_headers", status_code=201)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
) -> dict:
    response_headers = {}
    response_headers["Accept"] = accept
    response_headers["Content-Type"] = content_type
    response_headers["User-Agent"] = user_agent
    response_headers["Host"] = host
    return response_headers
