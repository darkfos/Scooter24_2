from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from src.database.models.brand import Brand
from src.store.tools import RedisTools
import pytest

redis: RedisTools = RedisTools()


@pytest.mark.asyncio
async def test_get_all_brands(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/brand/get_all_brands")

    assert req.status_code == 200 and "brands" in req.json()


@pytest.mark.asyncio
async def test_get_all_brands_2(
    async_client: AsyncClient, session: AsyncSession
) -> None:

    stmt = insert(Brand).values(name_brand="scooter24")
    await session.execute(stmt)
    await session.commit()

    await redis.delete_key("get_all_brands")

    req = await async_client.get(url="/api/v1/brand/get_all_brands")

    assert req.status_code == 200 and len(req.json()["brands"]) == 1


@pytest.mark.asyncio
async def test_get_brand_by_id(
    async_client: AsyncClient, session: AsyncSession
) -> None:

    req = await async_client.get(url="/api/v1/brand/get_brand_by_id/1")

    assert req.status_code == 200 and req.json()["name_brand"] == "scooter24"
