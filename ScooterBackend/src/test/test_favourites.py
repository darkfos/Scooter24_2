import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

TOKEN: str = ""


@pytest.mark.asyncio
async def test_all_favourites_user(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    req = await async_client.get(
        url="/api/v1/favourite/all/user"
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_no_create_favourite(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/unique/1")

    assert req.status_code == 404


@pytest.mark.asyncio
async def get_all_fav_by_not_admin(async_client: AsyncClient) -> None:
    req = await async_client.get(
        url="/api/v1/all",
        headers={"Authorization": "Bearer {}".format(TOKEN)},
    )

    assert req.status_code == 400
