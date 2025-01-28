from src.database.repository.brand_repository import Brand
from src.api.authentication.secure.authentication_service import (
    Authentication,
    AuthenticationEnum,
)
from src.store.tools import RedisTools
from src.api.dep.dependencies import IEngineRepository
from src.api.core.brand_app.schemas.brand_dto import BrandBase, AllBrands
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.api.core.brand_app.error.http_brand_exceptions import (
    BrandException,
)
from typing import NoReturn


auth: Authentication = Authentication()
redis: RedisTools = RedisTools()


class BrandService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def add_a_new_brand(
        engine: IEngineRepository,
        token: str,
        new_brand: BrandBase,
        token_data: dict = dict(),
    ) -> NoReturn:
        """
        Метод сервиса бренд - создание нового бренда
        """

        async with engine:

            # Проверка на администратора
            is_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:

                new_brand = Brand(name_brand=new_brand.name_brand)

                is_created = await engine.brand_repository.add_one(
                    data=new_brand
                )

                if is_created:
                    return
                await BrandException().no_create_a_new_brand()

            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_brand_by_id(
        engine: IEngineRepository, id_brand: int, redis_search_data: dict = {}
    ) -> BrandBase:
        """
        Метод сервиса бренд - получение бренда по id
        """

        async with engine:

            brand = await engine.brand_repository.find_one(other_id=id_brand)
            if brand:
                return BrandBase(name_brand=brand[0].name_brand)
            await BrandException().no_found_a_brand()

    @redis
    @staticmethod
    async def get_all_brands(
        engine: IEngineRepository, redis_search_data: dict = {}
    ) -> AllBrands:
        """
        Метод сервиса бренд - получение списка брендов
        """

        async with engine:

            brands = await engine.brand_repository.find_all()

            if brands:
                return AllBrands(
                    brands=[
                        BrandBase(name_brand=brand[0].name_brand)
                        for brand in brands
                    ]
                )
            return AllBrands(brands=[])

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_brand_by_id(
        engine: IEngineRepository,
        token: str,
        id_brand: int,
        token_data: dict = {},
    ) -> None:
        """
        Метод сервиса бренд - удаление бренда по идентификатору
        """

        async with engine:

            # Проверка на администратора
            is_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data["email"]
                )
            )

            if is_admin:

                is_deleted = await engine.brand_repository.delete_one(
                    other_id=id_brand
                )

                if is_deleted:
                    return

                await BrandException().no_delete_a_brand()

            await UserHttpError().http_user_not_found()
