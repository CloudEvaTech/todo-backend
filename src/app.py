from fastapi import FastAPI

from src.register.routers import router


def create_app() -> FastAPI:

    app = FastAPI(
        title="To-Do Application",
        description="A simple To-Do application built with FastAPI",
        version="1.0.0",
        summary="To-Do API",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.include_router(router, prefix="/api")

    return app


app = create_app()
