import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_new_category(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/api/v1/category/create",
        data={
            "name_category": "New category",
            "icon_category": "string"
        }
    )

    assert req.status_code == 401, "Категория была создана"


@pytest.mark.asyncio
async def test_get_category_icon(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/category/icon/2"
    )

    assert req.status_code == 404, "Категория не была найдена"


@pytest.mark.asyncio
async def test_get_all_categories(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/category/all"
    )

    assert req.json()["categories"] == [], "Категории были найдены"


@pytest.mark.asyncio
async def test_find_category_by_id(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/category/find/id/2"
    )

    assert req.status_code == 404, "Категория была найдена"


@pytest.mark.asyncio
async def test_update_category_name(async_client: AsyncClient) -> None:
    req = await async_client.patch(
        url="/api/v1/category/update/name",
        data={
            "name_category": "Электрика",
            "new_name_category": "Электрические запчасти"
        }
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_delete_category(async_client: AsyncClient) -> None:
    req = await async_client.delete(
        url="/api/v1/category/delete/2",
    )

    assert req.status_code == 401
