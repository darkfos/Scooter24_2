from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_type_worker(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/api/v1/type_worker/create", data={"name_type": "Грузчик"}
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_all_type_workers(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/type_worker/all")

    assert req.json()["type_worker"] == []


@pytest.mark.asyncio
async def test_get_unique_type_worker(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/type_worker/unique?id_type_worker=1",
    )

    assert req.status_code == 404


@pytest.mark.asyncio
async def test_delete_type_worker(async_client: AsyncClient) -> None:
    req = await async_client.delete(url="/api/v1/type_worker/delete?id_type=1")

    assert req.status_code == 401
