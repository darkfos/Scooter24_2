from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_vacancy(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/api/v1/vacancy/create",
        data={
            "salary_employee": 1,
            "description_vacancies": "string",
            "is_worked": "string",
            "type_work": {},
            "id_vacancy": 0,
        },
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_create_vacancy_req(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/api/v1/vacancy/create/req",
        data={
            "name_user": "Name vacancy",
            "email_user": "darkfos82@gmail.com",
            "telephone_user": "+79185922728",
            "experience_user": "Experience",
            "id_vacancy": 1,
        },
    )

    assert req.status_code == 422


@pytest.mark.asyncio
async def test_get_all_vacancy(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/vacancy/all")

    assert req.json()["vacancies"] == []


@pytest.mark.asyncio
async def test_unique_vacancy(async_client: AsyncClient) -> None:
    req = await async_client.get(url="/api/v1/vacancy/unique/2")

    assert req.status_code == 400


@pytest.mark.asyncio
async def test_update_vacancy(async_client: AsyncClient) -> None:
    req = await async_client.put(
        url="/api/v1/vacancy/update",
        data={
            "id": 2,
            "salary_employee": 19500,
            "description_vacancies": "Новая вакансия",
        },
    )

    assert req.status_code == 401


@pytest.mark.asyncio
async def test_delete_vacancy(async_client: AsyncClient) -> None:
    req = await async_client.delete(url="/api/v1/vacancy/delete/2")

    assert req.status_code == 401
