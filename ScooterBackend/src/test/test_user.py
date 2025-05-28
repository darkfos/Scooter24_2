from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_information_user(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/user/information")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_full_information_user(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/user/information/all")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_all_user_reviews(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/user/all/reviews")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_all_user_favourites(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/user/all/favourites")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_all_user_orders(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/user/all/orders")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_information_other_user(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/user/information/other/2")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_success_user_orders(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/v1/user/success/orders")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_update_user_information(async_client: AsyncClient) -> None:
    req = await async_client.put(
        url="/v1/user/update",
        data={
            "main_name_user": "string",
            "address": "string",
            "telephone": "string",
            "date_birthday": "2025-05-02",
            "date_update": "2025-05-01",
        },
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient) -> None:
    req = await async_client.delete(url="/v1/user/delete")

    assert req.status_code == 401
