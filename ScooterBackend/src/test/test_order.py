import datetime

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_get_all_orders(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/order/all/user")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_get_unique_order(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/order/unique/3")

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_delete_order(async_client: AsyncClient) -> None:
    req = await async_client.delete(url='/api/v1/order/delete/3')

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_create_order(async_client: AsyncClient) -> None:
    req = await async_client.post(url="/api/v1/order/create", data={
        "id_product": 3,
        "date_create": datetime.date.today()
    })

    assert req.status_code == 401