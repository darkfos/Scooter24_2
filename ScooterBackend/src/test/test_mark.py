import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from src.database.models.marks import Mark
from src.store.tools import RedisTools
from httpx import AsyncClient


redis: RedisTools = RedisTools()


@pytest.mark.asyncio
async def test_get_all_marks(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/mark/all")

    assert req.status_code == 200 and req.json().get("marks") == list()


@pytest.mark.asyncio
async def test_get_mark_by_id_no_created(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/mark/unique/1")

    assert req.status_code == 404


@pytest.mark.asyncio
async def test_get_marks_by_created(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    stmt = insert(Mark).values(name_mark="honda")
    await session.execute(stmt)
    await session.commit()

    await redis.delete_key(key="all_marks")

    req = await async_client.get(url="/v1/mark/all")
    assert req.status_code == 200 and len(req.json()["marks"]) == 1


@pytest.mark.asyncio
async def test_get_mark_by_id_created(async_client: AsyncClient) -> None:
    await redis.delete_key(key="mark_by_id_{}".format(1))
    req = await async_client.get(url="/v1/mark/unique/1")

    print(req)
    assert req.status_code == 200 and req.json()["name_mark"] == "honda"
