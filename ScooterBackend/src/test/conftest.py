# Entry point
import asyncio.events
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from src.database.mainbase import MainBase
from src.scooter_backend_application import ScooterBackendApplication
from typing import Final, AsyncGenerator
import pytest


app = ScooterBackendApplication().scooter24_app
TESTDATABASE: Final[str] = "sqlite+aiosqlite:///./testdb.db"

async_engine_for_test = create_async_engine(url=TESTDATABASE)
session = sessionmaker(
    bind=async_engine_for_test, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session() as sess:
        yield sess


@pytest.fixture(autouse=True, scope="session")
async def work_on_database() -> None:
    """
    Создание и удаление БД
    """

    async with async_engine_for_test.begin() as connection:
        await connection.run_sync(MainBase.metadata.create_all)
    yield  # work tests
    async with async_engine_for_test.begin() as connection:
        await connection.run_sync(MainBase.metadata.drop_all)


# SETUO
@pytest.fixture(autouse=True, scope="session")
def event_loop(request):
    """
    Main session for test
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app=app)
