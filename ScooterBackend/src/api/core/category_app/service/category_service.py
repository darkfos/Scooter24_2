import logging as logger
from typing import List, Union

from fastapi.responses import FileResponse
from fastapi import status

from src.database.repository.category_repository import Category
from src.api.core.category_app.schemas.category_dto import (
    CategoriesList,
    DataCategoryToUpdate,
    CategoryBase,
    CategoryIsCreated,
    CategoryIsUpdated,
    CategoryBaseData,
)
from src.api.core.subcategory_app.schemas.subcategory_dto import (
    SubCategoryAllData,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.api.core.category_app.error.http_category_exception import (
    CategoryHttpError,
)
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum

from src.store.tools import RedisTools

redis: RedisTools = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class CategoryService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_category(
        engine: IEngineRepository,
        token: str,
        new_category: CategoryBase,
        token_data: dict = dict(),
    ) -> CategoryIsCreated:
        """
        Метод сервиса для создания новой категории товаров
        :param engine:
        :param token:
        :param new_category:
        :return:
        """

        logging.info(
            msg=f"{CategoryService.__name__} Создание новой категории товара"
        )

        async with engine:
            find_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if find_admin:
                create_new_category = await engine.category_repository.add_one(
                    data=Category(**new_category.model_dump())
                )
                if create_new_category:
                    return CategoryIsCreated(is_created=True)
                await CategoryHttpError().http_failed_to_create_a_new_category()

            logging.critical(
                msg=f"{CategoryService.__name__} "
                f"Не удалось создать новую категорию товара"
            )
            await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_icon_category(
        engine: IEngineRepository, id_category: int
    ) -> FileResponse:

        logger.info(
            msg=f"{CategoryService.__name__} Получение иконки категории"
        )

        async with engine:
            category_data = await engine.category_repository.find_one(
                other_id=id_category
            )
            if category_data:
                return FileResponse(
                    path="src/static/images/{}".format(
                        category_data[0].icon_category
                    ),
                    filename="logo_category",
                    media_type="image/jpeg",
                    status_code=status.HTTP_200_OK,
                )

            await CategoryHttpError().http_not_found_a_icon()

    @redis
    @staticmethod
    async def find_all_categories(
        engine: IEngineRepository, redis_search_data: str
    ):
        """
        Метод сервиса для получения всех категорий
        :param session:
        :return:
        """

        logging.info(
            msg=f"{CategoryService.__name__} Получение всех категорий"
        )
        async with engine:
            categories: List[CategoryBase] = (
                await engine.category_repository.find_all_with_sb()
            )
            result = CategoriesList(
                categories=[
                    CategoryBase(
                        name_category=category[0].name_category,
                        id_category=category[0].id,
                        icon_category=(
                            category[0].icon_category
                            if category[0].icon_category is not None
                            else ""
                        ),
                        subcategory=[
                            SubCategoryAllData(
                                name=sb.name,
                                id_category=sb.id_category,
                                id_subcategory=sb.id,
                            )
                            for sb in category[0].subcategory_data
                        ],
                    )
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

        logging.info(
            msg=f"{CategoryService.__name__} "
            f"Поиск категории по id={id_category}"
        )
        async with engine:
            category: Union[None, Category] = (
                await engine.category_repository.find_one(other_id=id_category)
            )
            if category:
                return CategoryBaseData(
                    name_category=category[0].name_category,
                    icon_category=category[0].icon_category,
                )
            logging.critical(
                msg=f"{CategoryService.__name__} "
                f"Не удалось найти категорию по id={id_category}"
            )
            await CategoryHttpError().http_category_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_category(
        engine: IEngineRepository,
        token: str,
        data_to_update: DataCategoryToUpdate,
        token_data: dict = dict(),
    ) -> CategoryIsUpdated:
        """
        Метод сервиса для обновления категории
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{CategoryService.__name__} Обновление названия категории"
        )
        async with engine:
            is_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    token_data.get("email")
                )
            )

            if is_admin:
                find_category: Union[None, Category] = (
                    await engine.category_repository.find_by_name(
                        category_name=data_to_update.name_category,
                        type_find=True,
                    )
                )

                if find_category:
                    is_updated = await engine.category_repository.update_one(
                        other_id=find_category.id,
                        data_to_update={
                            "name_category": data_to_update.new_name_category
                        },
                    )
                    return CategoryIsUpdated(is_updated=is_updated)
            logging.critical(
                msg=f"{CategoryService.__name__} "
                f"Не удалось обновить данные по категории"
            )
            await CategoryHttpError().http_category_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_category(
        engine: IEngineRepository,
        id_category: int,
        token: str,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для удаления категории по id
        :param session:
        :param id_category:
        :return:
        """

        logging.info(
            msg=f"{CategoryService.__name__} "
            f"Удаление категории по id={id_category}"
        )
        async with engine:
            is_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    token_data.get("email")
                )
            )
            if is_admin:
                is_del = await engine.category_repository.delete_one(
                    other_id=id_category
                )
                if is_del:
                    return
                await CategoryHttpError().http_failed_to_delete_category()
            logging.critical(
                msg=f"{CategoryService.__name__} "
                f"Не удалось удалить категорию по "
                f"id={id_category}"
            )
            await UserHttpError().http_user_not_found()
