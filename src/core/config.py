import tomllib
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Env(StrEnum):
    DEV = "dev"


class Settings(BaseSettings):
    SECRET_KEY: str = Field(default="ea90084454f1f94244f779d605286ae482ffb1f33570dcd1f6a683e5c002b492")
    SECURITY_BCRYPT_ROUNDS: int = Field(default=4)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=120)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=11520)
    BACKEND_CORS: list[str] = Field(default=["*"])
    ALLOWED_HOST: list[str] = Field(default=["*"])
    BASE_URL: str = Field(default="http://localhost:8000")

    WEB_SENTRY_DSN: str | None = Field(default=None)
    SENTRY_SAMPLE_RATE: float = Field(default=1.0, gt=0.0, le=1.0)
    SENTRY_TRACES_SAMPLE_RATE: float | None = Field(default=None, gt=0.0, le=1.0)

    SQLALCHEMY_DATABASE_URI: str = Field(
        default="sqlite+aiosqlite:///./sql_app.db",
    )
    DATABASE_POOL_SIZE: int | None = Field(default=50)
    DATABASE_POOL_MAX_OVERFLOW: int | None = Field(default=10)

    ENV: str = _Env.DEV.name
    RUNNING_MODE: Literal["uvicorn", "gunicorn"] | None = Field(default="uvicorn")
    WORKERS: int | None = Field(default=1, gt=0)
    LISTENING_HOST: str = Field(default="0.0.0.0")
    LISTENING_PORT: int = Field(default=8000, gt=0, le=65535)


settings = Settings()
