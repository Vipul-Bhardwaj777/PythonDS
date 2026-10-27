from fastapi import APIRouter, FastAPI
from app.features.books_crud.DB.main import init_db
from .features.books_crud.routes import router as books_router
from .features.first_rest.routes import router as rest_router
from .features.auth.routes import router as auth_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    # await init_db()
    yield
    print("Server stopped")


version = "v1"

app = FastAPI(title="FastAPI Backend", version=version, lifespan=life_span)
api = APIRouter(prefix=f"/api/{version}")

api.include_router(books_router, prefix=f"/books", tags=["Books Crud"])
api.include_router(rest_router, prefix=f"/rest", tags=["Rest"])
api.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.include_router(api)


@app.get("/")
async def root_read():
    return {"server": "ok"}
