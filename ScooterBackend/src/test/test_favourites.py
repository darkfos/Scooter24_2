import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

TOKEN: str = ""


@pytest.mark.asyncio
async def test_all_favourites_user(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    req = await async_client.get(
        url="/api/v1/favourite/get_all_favourites_by_user_id"
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_favourites_user_by_log(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    req_to_auth = await async_client.post(
        url="/auth/login",
        data={"username": "darkflsd@list.ru", "password": "90034jkajkdsad"},
    )

    assert req_to_auth.status_code == 201
    global TOKEN
    TOKEN = req_to_auth.json().get("access_token")

    req_to_my_fav = await async_client.get(
        url="/api/v1/favourite/get_all_favourites_by_user_id",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    assert (
        req_to_my_fav.status_code == 200
        and req_to_my_fav.json()["favourites"] == list()
    )


@pytest.mark.asyncio
async def test_no_create_favourite(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/get_favourite_data_for_id/1")

    assert req.status_code == 404


@pytest.mark.asyncio
async def get_all_fav_by_not_admin(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/get_all_favourites",
        headers={"Authorization": "Bearer {}".format(TOKEN)},
    )

    assert req.status_code == 400
