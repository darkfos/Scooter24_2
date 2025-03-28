from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from database.models.model import Model
import pytest


@pytest.mark.asyncio
async def test_get_all_models(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/model/get_all_models")

    assert req.status_code == 200 and len(req.json()["all_models"]) == 0


@pytest.mark.asyncio
async def test_get_model_by_id_f(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/model/get_model_by_id/1")

    assert req.status_code == 400


@pytest.mark.asyncio
async def test_get_model_by_id_t(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    stmt = insert(Model).values(name_model="honkai", id_mark=1)
    await session.execute(stmt)
    await session.commit()

    req = await async_client.get(url="/api/v1/model/get_model_by_id/1")

    assert req.status_code == 200 and req.json()["name_model"] == "honkai"
