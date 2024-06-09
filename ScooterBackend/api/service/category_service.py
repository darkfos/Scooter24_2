#System
import datetime
from typing import List, Union, Dict

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.database.repository.category_repository import CategoryRepository, Category
from ScooterBackend.api.dto.category_dto import *
from ScooterBackend.database.repository.admin_repository import AdminRepository
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.api.authentication.hashing import CryptographyScooter
from ScooterBackend.api.exception.http_category_exception import CategoryHttpError
from ScooterBackend.api.exception.http_user_exception import UserHttpError
from ScooterBackend.api.exception.http_category_exception import CategoryHttpError


class CategoryService:

    @staticmethod
    async def create_category(session: AsyncSession, token: str, new_category: CategoryBase) -> CategoryIsCreated:
        """
        Метод сервиса для создания новой категории товаров
        :param session:
        :param token:
        :param new_category:
        :return:
        """

        #Decode jwt token
        jwt_data: Dict[str, Union[str, int, datetime.date]] = await Authentication().decode_jwt_token(
            token=token,
            type_token="access"
        )

        #Find user in Admin table
        adm = AdminRepository(session=session)
        cat = CategoryRepository(session=session)
        find_admin = await adm.find_admin_by_email_and_password(email=jwt_data.get("email"))

        if find_admin:
            create_new_category = await cat.add_one(data=Category(**new_category.model_dump()))
            if create_new_category:
                return CategoryIsCreated(
                    is_created=create_new_category
                )
            await CategoryHttpError().http_failed_to_create_a_new_category()

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def find_category_by_name(session: AsyncSession, name_category: str) -> CategoryIsFinded:
        """
        Метод сервиса для поиска категории по названию
        :param session:
        :param name_category:
        :return:
        """

        #Find category
        is_found: bool = await CategoryRepository(session=session).find_by_name(category_name=name_category)
        return CategoryIsFinded(
            is_find=is_found
        )

    @staticmethod
    async def find_all_categories(session: AsyncSession):
        """
        Метод сервиса для получения всех категорий
        :param session:
        :return:
        """

        #Get categories
        categories: List[CategoryBase] = await CategoryRepository(session=session).find_all()
        result = [category for category in categories[0]]
        return result

    @staticmethod
    async def find_by_id(session: AsyncSession, id_category: int) -> CategoryBase:
        """
        Метод сервиса для поиска категории по id
        :param session:
        :param id_category:
        :return:
        """

        #Get category
        category: Union[None, Category] = await CategoryRepository(session=session).find_one(other_id=id_category)
        if category:
            return CategoryBase(
                name_category=category[0].name_category
            )

        await CategoryHttpError().http_category_not_found()

    @staticmethod
    async def update_category(session: AsyncSession, token: str, data_to_update: DataCategoryToUpdate) -> CategoryIsUpdated:
        """
        Метод сервиса для обновления токена
        :param session:
        :param token:
        :return:
        """

        #Decode token
        token_data: Dict[str, str] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Find admin
        adm = AdminRepository(session=session)
        cat = CategoryRepository(session=session)
        is_admin = await adm.find_admin_by_email_and_password(token_data.get("email"))

        if is_admin:
            #Find category
            find_category: Union[None, Category] = await cat.find_by_name(category_name=data_to_update.name_category, type_find=True)

            if find_category:
                #Update data
                is_updated = await cat.update_one(other_id=find_category.id, data_to_update={"name_category": data_to_update.new_name_category})
                return CategoryIsUpdated(
                    is_updated=is_updated
                )

        await CategoryHttpError().http_category_not_found()

    @staticmethod
    async def delete_category(session: AsyncSession, id_category: int, token: str) -> None:
        """
        Метод сервиса для удаления категории по id
        :param session:
        :param id_category:
        :return:
        """

        #Decode token
        token_data: Dict[str, str] = await Authentication().decode_jwt_token(token=token, type_token="access")
        is_admin = await AdminRepository(session=session).find_admin_by_email_and_password(token_data.get("email"))
        if is_admin:
            is_del = await CategoryRepository(session=session).delete_one(other_id=id_category)
            if is_del:
                return
            await CategoryHttpError().http_failed_to_delete_category()
        await UserHttpError().http_user_not_found()