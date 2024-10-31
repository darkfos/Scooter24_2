from httpx import AsyncClient
from typing import Union
import pytest


USERTOKEN: Union[str, None] = None
ADMINTOKEN: Union[str, None] = None


@pytest.mark.asyncio
async def test_get_all_products(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/product/get_all_products")

    assert req.status_code == 200 and len(req.json()["products"]) == 0


@pytest.mark.asyncio
async def test_get_product_by_category(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/get_products_by_category",
        params={"category_data": "Трансмиссия"},
    )

    assert req.status_code == 200 and req.json()["products"] == []


@pytest.mark.asyncio
async def test_get_product_by_id(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/get_products_by_category",
        params={"category_data": 1},
    )

    assert req.status_code == 200


@pytest.mark.asyncio
async def test_get_product_by_filters(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/get_products_by_filter",
        params={
            "id_category": 1,
            "min_price": 400,
            "max_price": 800,
        },
    )

    assert req.status_code == 200 and req.json()["products"] == []


@pytest.mark.asyncio
async def test_product_is_exists(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/product_is_exists/Трансмиссия"
    )

    assert req.status_code == 404


@pytest.mark.asyncio
async def test_product_all_information(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/product/get_all_information_about_product",
        params={"id_product": 1},
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_product_recommended_products(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/product/get_recommended_products")

    assert req.status_code == 404


@pytest.mark.asyncio
async def test_get_new_products(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/product/new_products")

    assert req.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_by_user(async_client: AsyncClient) -> None:
    req_auth_user = await async_client.post(
        url="/auth/login",
        data={"username": "darkflsd@list.ru", "password": "90034jkajkdsad"},
    )

    global USERTOKEN
    USERTOKEN = req_auth_user.json()["access_token"]

    req_delete_product = await async_client.delete(
        url="/api/v1/product/delete_product/1",
        headers={"Authorization": "Bearer {}".format(USERTOKEN)},
    )

    assert req_delete_product.status_code == 404
