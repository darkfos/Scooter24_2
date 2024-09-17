###########МОДУЛЬ ДЛЯ НАЧАЛЬНОЙ ЗАПИСИ ДАННЫХ################

from src.database.db_worker import db_work
import aiohttp
import asyncio


async def write_in_db():
    session = await db_work.get_session()

    all_categories: list = [
        "Аксессуары",
        "Двигатель",
        "Подвеска",
        "Топливная Система",
        "Тормозная Система",
        "Трансмиссия",
        "Электрика",
        "Все",
    ]

    jwt_token: str = ""

    # Запись данных
    async with aiohttp.ClientSession() as session:
        # Токен
        async with session.post(
            url="https://scooter24-2.onrender.com/api/v1/auth/login",
            data={"username": "test@mail.ru", "password": "test123"},
        ) as j_session:
            jwt_token = (await j_session.json()).get("access_token")

    async with aiohttp.ClientSession(
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }
    ) as session2:
        for category in all_categories:
            async with session2.post(
                url="https://scooter24-2.onrender.com/api/v1/category/create_new_category",
                json={"name_category": category},
            ) as data:
                print(data.status)


if __name__ == "__main__":
    asyncio.run(write_in_db())
