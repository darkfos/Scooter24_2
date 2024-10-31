import datetime
from httpx import AsyncClient
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.user_type import UserType
from src.database.models.user import User
from src.api.authentication.hash_service.hashing import CryptographyScooter
import pytest


REFRESH_TOKEN_LOCAL: str = ""


@pytest.mark.asyncio
async def test_user_registration_f(async_client: AsyncClient) -> None:
    req = await async_client.post(
        url="/auth/registration",
        json={
            "email_user": "3kkfjsdf@list.com",
            "password_user": "chaiki8293",
            "name_user": "dsadaf",
            "surname_user": "sdasd",
            "main_name_user": "gfdgfdgdf",
            "date_registration": "2024-10-25",
        },
    )
    assert req.status_code == 201


@pytest.mark.asyncio
async def test_user_registration_t(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    stmt = insert(UserType).values(id=1, name_type="user")
    await session.execute(stmt)
    await session.commit()
    result_to_add = (await session.execute(select(UserType))).all()
    req = await async_client.post(
        url="/auth/registration",
        json={
            "email_user": "user@example.com",
            "password_user": "string",
            "name_user": "string",
            "surname_user": "string",
            "main_name_user": "string",
            "date_registration": "2024-10-31",
        },
    )

    assert result_to_add[0][0].id == 1
    assert req.status_code == 201


@pytest.mark.asyncio
async def test_user_auth(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    req_auth = await async_client.post(
        url="/login",
        data={"username": "3kkfjsdf@list.com", "password": "chaiki8293"},
    )

    assert req_auth.status_code == 404


@pytest.mark.asyncio
async def test_user_auth_t(
    async_client: AsyncClient, session: AsyncSession
) -> None:
    hashed_password = CryptographyScooter().hashed_password(
        password="90034jkajkdsad"
    )
    stmt = insert(User).values(
        User(
            is_active=True,
            id_type_user=1,
            email_user="darkflsd@list.ru",
            password_user=hashed_password,
            name_user="new_user",
            surname_user="usernsd",
            main_name_user="agata kristi",
            date_registration=datetime.date.today(),
            date_update=datetime.date.today(),
        ).read_model()
    )

    await session.execute(stmt)
    await session.commit()

    req_auth = await async_client.post(
        url="/auth/login",
        data={"username": "darkflsd@list.ru", "password": "90034jkajkdsad"},
    )

    global REFRESH_TOKEN_LOCAL
    REFRESH_TOKEN_LOCAL = req_auth.json()["refresh_token"]
    assert req_auth.status_code == 201


@pytest.mark.asyncio
async def update_refresh_token(async_client: AsyncClient) -> None:

    req_for_update_token = await async_client.post(
        url="/update_token", params={"refresh_token": REFRESH_TOKEN_LOCAL}
    )

    assert req_for_update_token.status_code == 201
