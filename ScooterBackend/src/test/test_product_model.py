from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_product_model(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/v1/product_model/create",
        data={"id_product": 101, "id_model": 2},
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_get_all_product_models_by_id_product(
    async_client: AsyncClient,
) -> None:
    req = await async_client.get(url="/v1/product_model/all/id/109")

    assert req.status_code == 400


@pytest.mark.asyncio
async def test_get_all_product_models(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/product_model/all")

    assert req.json()["all_models"] == []


@pytest.mark.asyncio
async def test_delete_product_model(async_client: AsyncClient) -> None:
    req = await async_client.delete(url="/v1/product_model/delete/1")

    assert req.status_code == 401
