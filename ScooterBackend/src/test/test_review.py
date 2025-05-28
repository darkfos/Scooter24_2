from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_review(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/api/v1/review/create",
        data={
            "text_review": "Test text",
            "estimation_review": 10,
            "id_product": 1,
        },
    )

    assert req.status_code == 401, "Отзыв был создан!"


@pytest.mark.asyncio
async def test_get_all_review_by_id_product(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/review/all/product/109")

    assert (
        req.status_code == 200 and req.json()["reviews"] == []
    ), "Отзывы не были найдены"


@pytest.mark.asyncio
async def test_get_all_reviews(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/review/all")

    assert req.json() == [], "Отзывы были найдены"


@pytest.mark.asyncio
async def test_get_unique_review_by_id(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/review/unique/2")

    assert req.status_code == 404, "Отзыв был найден"


@pytest.mark.asyncio
async def test_delete_review(async_client: AsyncClient) -> None:
    req = await async_client.delete(url="/api/v1/review/delete/2")

    assert req.status_code == 401, "Отзыв был удален"
