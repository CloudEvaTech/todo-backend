import logging
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

from src.core.models.base import Base
from src.features.authentication.models.user import User
from src.features.to_do.models.tasks import Status, ToDoItem

async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    future=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_POOL_MAX_OVERFLOW,
)
async_session = async_sessionmaker(
    async_engine, autoflush=False, expire_on_commit=False
)


async def get_session() -> AsyncGenerator["AsyncSession", None]:
    async with async_session() as session:
        yield session


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
