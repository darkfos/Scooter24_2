# Entry point
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from httpx import AsyncClient, ASGITransport
from database.mainbase import MainBase
from scooter_backend_application import ScooterBackendApplication
from database.db_worker import db_work
from typing import Final, Generator, AsyncGenerator
import pytest


app = ScooterBackendApplication().scooter24_app
TESTDATABASE: Final[str] = "sqlite+aiosqlite:///./testdb.db"

engine_for_test = create_async_engine(
    url=TESTDATABASE, connect_args={"timeout": 30}
)
async_session = async_sessionmaker(
    bind=engine_for_test,
    class_=AsyncSession,
    expire_on_commit=False,
)
db_work.async_session = async_session


@pytest.fixture(autouse=True, scope="session")
async def work_on_database() -> None:
    """
    Создание и удаление БД
    """

    async with engine_for_test.begin() as connection:
        await connection.run_sync(MainBase.metadata.create_all)
    yield
    async with engine_for_test.begin() as connection:
        await connection.run_sync(MainBase.metadata.drop_all)


@pytest.fixture(scope="session")
async def session() -> AsyncGenerator:
    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
async def async_client() -> Generator:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        yield ac
