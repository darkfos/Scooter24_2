from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_subcategory(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/api/v1/sub_category/create",
        data={"name": "New subcategory", "id_category": 2},
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_get_all_subcategories(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/sub_category/all")

    assert len(req.json()["all_subcategory"]) == 0


@pytest.mark.asyncio
async def test_get_all_subcategories_by_id_category(
    async_client: AsyncClient,
) -> None:
    req = await async_client.get(url="/api/v1/sub_category/all/category/2")

    assert req.status_code == 400


@pytest.mark.asyncio
async def test_delete_subcategory_by_id(async_client: AsyncClient) -> None:
    req = await async_client.delete(url="/api/v1/sub_category/delete/2")

    assert req.status_code == 401
