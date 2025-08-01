from fastapi import APIRouter

from src.features.authentication.api.auth import router as auth_router
from src.features.to_do.api.todo import router as todo_router


def register_v1_router() -> APIRouter:
    root_router = APIRouter()
    root_router.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
    root_router.include_router(todo_router, prefix="/v1/todo", tags=["To-Do"])
    return root_router


router = register_v1_router()
