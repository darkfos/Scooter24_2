# System
import datetime, logging
from typing import List, Union, Dict, Type
from typing import List, Union, Dict, Coroutine, Any, Type

# Other libraries
...

# Local
from src.database.repository.category_repository import Category
from src.api.core.category_catalog.schemas.category_dto import *
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.category_catalog.error.http_category_exception import CategoryHttpError
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.core.category_catalog.error.http_category_exception import CategoryHttpError
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum

# Redis
from src.store.tools import RedisTools

redis: RedisTools = RedisTools()
auth: Authentication = Authentication()


class CategoryService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_category(
        engine: IEngineRepository, token: str, new_category: CategoryBase, token_data: dict = dict()
    ) -> CategoryIsCreated:
        """
        Метод сервиса для создания новой категории товаров
        :param engine:
        :param token:
        :param new_category:
        :return:
        """

        logging.info(msg=f"{CategoryService.__name__} Создание новой категории товара")

        async with engine:
            # Find user in Admin table
            find_admin = await engine.admin_repository.find_admin_by_email_and_password(
                email=token_data.get("email")
            )

            if find_admin:
                create_new_category = await engine.category_repository.add_one(
                    data=Category(**new_category.model_dump())
                )
                if create_new_category:
                    return CategoryIsCreated(is_created=True)
                await CategoryHttpError().http_failed_to_create_a_new_category()

            logging.critical(msg=f"{CategoryService.__name__} Не удалось создать новую категорию товара")
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def find_category_by_name(
        engine: IEngineRepository, name_category: str, redis_search_data: str
    ) -> CategoryIsFinded:
        """
        Метод сервиса для поиска категории по названию
        :param session:
        :param name_category:
        :return:
        """

        logging.info(msg=f"{CategoryService.__name__} Поиск категории по названию name_category={name_category}")
        async with engine:
            # Find category
            is_found: bool = await engine.category_repository.find_by_name(
                category_name=name_category
            )
            return CategoryIsFinded(is_find=is_found)

    @redis
    @staticmethod
    async def find_all_categories(engine: IEngineRepository, redis_search_data: str):
        """
        Метод сервиса для получения всех категорий
        :param session:
        :return:
        """

        logging.info(msg=f"{CategoryService.__name__} Получение всех категорий")
        async with engine:
            # Get categories
            categories: List[CategoryBase] = await engine.category_repository.find_all()
            result = CategoriesList(
                categories=[
                    CategoryBase(name_category=category[0].name_category)
                    for category in categories
                ]
            )
            return result

    @redis
    @staticmethod
    async def find_by_id(
        engine: IEngineRepository, id_category: int, redis_search_data: str
    ) -> CategoryBase:
        """
        Метод сервиса для поиска категории по id
        :param session:
        :param id_category:
        :return:
        """

        logging.info(msg=f"{CategoryService.__name__} Поиск категории по id={id_category}")
        async with engine:
            # Get category
            category: Union[None, Category] = await engine.category_repository.find_one(
                other_id=id_category
            )
            if category:
                return CategoryBase(name_category=category[0].name_category)
            logging.critical(msg=f"{CategoryService.__name__} Не удалось найти категорию по id={id_category}")
            await CategoryHttpError().http_category_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_category(
        engine: IEngineRepository, token: str, data_to_update: DataCategoryToUpdate, token_data: dict = dict()
    ) -> CategoryIsUpdated:
        """
        Метод сервиса для обновления категории
        :param session:
        :param token:
        :return:
        """

        logging.info(msg=f"{CategoryService.__name__} Обновление названия категории")
        async with engine:

            # Find admin
            is_admin = await engine.admin_repository.find_admin_by_email_and_password(
                token_data.get("email")
            )

            if is_admin:
                # Find category
                find_category: Union[None, Category] = (
                    await engine.category_repository.find_by_name(
                        category_name=data_to_update.name_category, type_find=True
                    )
                )

                if find_category:
                    # Update data
                    is_updated = await engine.category_repository.update_one(
                        other_id=find_category.id,
                        data_to_update={
                            "name_category": data_to_update.new_name_category
                        },
                    )
                    return CategoryIsUpdated(is_updated=is_updated)
            logging.critical(msg=f"{CategoryService.__name__} Не удалось обновить данные по категории")
            await CategoryHttpError().http_category_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_category(
        engine: IEngineRepository, id_category: int, token: str, token_data: dict = dict()
    ) -> None:
        """
        Метод сервиса для удаления категории по id
        :param session:
        :param id_category:
        :return:
        """

        logging.info(msg=f"{CategoryService.__name__} Удаление категории по id={id_category}")
        async with engine:
            is_admin = await engine.admin_repository.find_admin_by_email_and_password(
                token_data.get("email")
            )
            if is_admin:
                is_del = await engine.category_repository.delete_one(
                    other_id=id_category
                )
                if is_del:
                    return
                await CategoryHttpError().http_failed_to_delete_category()
            logging.critical(msg=f"{CategoryService.__name__} Не удалось удалить категорию по id={id_category}")
            await UserHttpError().http_user_not_found()
