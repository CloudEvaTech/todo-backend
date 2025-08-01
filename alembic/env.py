from logging.config import fileConfig
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from alembic import context

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models and Base for autogenerate support
from src.features.authentication.models import User
from src.features.to_do.models import ToDoItem, Status
from src.core.models.base import Base

# Set target_metadata for autogenerate
target_metadata = Base.metadata  # This should point to your SQLAlchemy Base metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Enable for better column type comparison
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations(connectable: AsyncEngine):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Enable for better column type comparison
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode using async engine."""
    # Get the URL from alembic.ini or override it here
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_async_engine(url)

    # Run the async migrations
    asyncio.run(run_async_migrations(connectable))

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()