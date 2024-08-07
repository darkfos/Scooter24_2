#System
import datetime
from typing import List, Union, Dict

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from database.repository.category_repository import CategoryRepository, Category
from api.dto.category_dto import *
from database.repository.admin_repository import AdminRepository
from api.authentication.authentication_service import Authentication
from api.authentication.hashing import CryptographyScooter
from api.exception.http_category_exception import CategoryHttpError
from api.exception.http_user_exception import UserHttpError
from api.exception.http_category_exception import CategoryHttpError
from api.dep.dependencies import EngineRepository, IEngineRepository


class CategoryService:

    @staticmethod
    async def create_category(
        engine: IEngineRepository,
        token: str,
        new_category: CategoryBase
    ) -> CategoryIsCreated:
        """
        Метод сервиса для создания новой категории товаров
        :param engine:
        :param token:
        :param new_category:
        :return:
        """

        #Decode jwt token
        jwt_data: Dict[str, Union[str, int, datetime.date]] = await Authentication().decode_jwt_token(
            token=token,
            type_token="access"
        )

        async with engine:
            #Find user in Admin table
            find_admin = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if find_admin:
                create_new_category = await engine.category_repository.add_one(data=Category(**new_category.model_dump()))
                if create_new_category:
                    return CategoryIsCreated(
                        is_created=True
                    )
                await CategoryHttpError().http_failed_to_create_a_new_category()

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def find_category_by_name(engine: IEngineRepository, name_category: str) -> CategoryIsFinded:
        """
        Метод сервиса для поиска категории по названию
        :param session:
        :param name_category:
        :return:
        """

        async with engine:
            #Find category
            is_found: bool = await engine.category_repository.find_by_name(category_name=name_category)
            return CategoryIsFinded(
                is_find=is_found
            )

    @staticmethod
    async def find_all_categories(engine: IEngineRepository):
        """
        Метод сервиса для получения всех категорий
        :param session:
        :return:
        """

        async with engine:
            #Get categories
            categories: List[CategoryBase] = await engine.category_repository.find_all()
            result = [category[0] for category in categories]
            return result

    @staticmethod
    async def find_by_id(engine: IEngineRepository, id_category: int) -> CategoryBase:
        """
        Метод сервиса для поиска категории по id
        :param session:
        :param id_category:
        :return:
        """

        async with engine:
            #Get category
            category: Union[None, Category] = await engine.category_repository.find_one(other_id=id_category)
            if category:
                return CategoryBase(
                    name_category=category[0].name_category
                )

            await CategoryHttpError().http_category_not_found()

    @staticmethod
    async def update_category(engine: IEngineRepository, token: str, data_to_update: DataCategoryToUpdate) -> CategoryIsUpdated:
        """
        Метод сервиса для обновления токена
        :param session:
        :param token:
        :return:
        """

        async with engine:
            #Decode token
            token_data: Dict[str, str] = await Authentication().decode_jwt_token(token=token, type_token="access")

            #Find admin
            is_admin = await engine.admin_repository.find_admin_by_email_and_password(token_data.get("email"))

            if is_admin:
                #Find category
                find_category: Union[None, Category] = await engine.category_repository.find_by_name(category_name=data_to_update.name_category, type_find=True)

                if find_category:
                    #Update data
                    is_updated = await engine.category_repository.update_one(other_id=find_category.id, data_to_update={"name_category": data_to_update.new_name_category})
                    return CategoryIsUpdated(
                        is_updated=is_updated
                    )

            await CategoryHttpError().http_category_not_found()

    @staticmethod
    async def delete_category(engine: IEngineRepository, id_category: int, token: str) -> None:
        """
        Метод сервиса для удаления категории по id
        :param session:
        :param id_category:
        :return:
        """

        async with engine:
            #Decode token
            token_data: Dict[str, str] = await Authentication().decode_jwt_token(token=token, type_token="access")
            is_admin = await engine.admin_repository.find_admin_by_email_and_password(token_data.get("email"))
            if is_admin:
                is_del = await engine.category_repository.delete_one(other_id=id_category)
                if is_del:
                    return
                await CategoryHttpError().http_failed_to_delete_category()
            await UserHttpError().http_user_not_found()