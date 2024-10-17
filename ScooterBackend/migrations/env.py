import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from src.settings.database_settings.database_settings import DatabaseSettings


# Tables
from src.database.models.subcategory import SubCategory  # noqa
from src.database.models.user import User  # noqa
from src.database.models.order import Order  # noqa
from src.database.models.product import Product  # noqa
from src.database.models.history_buy import HistoryBuy  # noqa
from src.database.models.review import Review  # noqa
from src.database.models.favourite import Favourite  # noqa
from src.database.models.category import Category  # noqa
from src.database.models.type_worker import TypeWorker  # noqa
from src.database.models.vacancies import Vacancies  # noqa
from src.database.models.brand import Brand  # noqa
from src.database.models.marks import Mark  # noqa
from src.database.models.model import Model  # noqa
from src.database.models.subcategory import SubCategory  # noqa
from src.database.models.sub_sub_category import SubSubCategory  # noqa
from src.database.models.product_models import ProductModels  # noqa
from src.database.models.user_type import UserType  # noqa

# Database for migrations
from src.database.mainbase import MainBase

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# URL to database
config.set_main_option("sqlalchemy.url", DatabaseSettings().db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = MainBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
