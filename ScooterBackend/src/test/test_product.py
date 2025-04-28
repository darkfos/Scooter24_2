from httpx import AsyncClient
from typing import Union
import pytest


USERTOKEN: Union[str, None] = None
ADMINTOKEN: Union[str, None] = None


@pytest.mark.asyncio
async def test_get_all_products(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/all/category",
        params={"category_data": "Трансмиссия"},
    )

    assert req.status_code == 200 and len(req.json()["products"]) == 0


@pytest.mark.asyncio
async def test_get_product_by_category(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/all/category",
        params={"category_data": "Трансмиссия"},
    )

    assert req.status_code == 200 and req.json()["products"] == []


@pytest.mark.asyncio
async def test_get_product_by_id(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/all/category",
        params={"category_data": 1},
    )

    assert req.status_code == 200


@pytest.mark.asyncio
async def test_get_product_by_filters(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/all/filter",
        params={
            "id_category": 1,
            "min_price": 400,
            "max_price": 800,
        },
    )

    assert req.status_code == 200 and req.json()["products"] == []


@pytest.mark.asyncio
async def test_product_is_exists(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/product/exists/Трансмиссия")

    assert req.status_code == 404


@pytest.mark.asyncio
async def test_product_all_information(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/information/full",
        params={"id_product": 1},
    )

    assert req.status_code == 404


@pytest.mark.asyncio
async def test_product_recommended_products(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/product/recommends")

    assert req.status_code == 200


@pytest.mark.asyncio
async def test_get_new_products(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/product/new")

    assert req.status_code == 404
