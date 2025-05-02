from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_user_type(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/api/v1/user_type/create",
        data={
            "name_type": "Модератор"
        }
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_get_all_user_types(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/user_type/all"
    )

    assert req.status_code == 200 and req.json()["user_types"] == []