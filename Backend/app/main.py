from fastapi import FastAPI, Header
from typing import Optional
from app.features.books_crud.routes import router as books_router
from app.schema import TodoReq, TodoRes

app = FastAPI(title="FastAPI Backend", version="0.1.0")
app.include_router(books_router)


@app.get("/")
async def root_read():
    return {"server": "ok"}


@app.get("/greet/{state}")
async def greet(city: str, state: str, name: Optional[str] = "User") -> dict:
    return {"message": f"Hii {name} from {city}, {state}!"}


@app.post("/create_todo", response_model=TodoRes)
async def create_todo(data: TodoReq) -> TodoRes:
    return {"message": "Todo created!"}


@app.get("/get_headers", status_code=201)
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
