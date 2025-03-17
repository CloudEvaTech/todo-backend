from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title = "TODO Application",
    description = "A TODO Application with all CRUD operations"
)

app.include_router(router)