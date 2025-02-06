# System
from typing import List, Type
import logging as logger

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

# Local
from src.database.models.category import Category
from src.database.repository.general_repository import GeneralSQLRepository


logging = logger.getLogger(__name__)


class CategoryRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Category] = Category
        super().__init__(session=session, model=self.model)

    async def find_by_name(
        self, category_name: str, type_find: bool = False
    ) -> bool:
        """
        Поиск категории по названию
        :param category_name:
        :return:
        """

        # Logging
        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Осуществлен поиск категории"
            f" по названию "
            f"category_name={category_name},"
            f" type_find={type_find}"
        )

        stmt = select(Category).where(Category.name_category == category_name)
        result = await self.async_session.execute(stmt)
        result_data = result.one_or_none()

        if type_find and result_data:
            return result_data[0].id

        logging.critical(
            msg=f"{self.__class__.__name__} "
            f"Не удалось найти категорию"
            f" по названию "
            f"category_name={category_name},"
            f" type_find={type_find}"
        )
        return False

    async def find_all_with_sb(self):
        """
        Получение всех категорий с данными о подкатегориях
        :return:
        """

        stmt = select(Category).options(
            joinedload(Category.subcategory_data)
        )

        result = await self.async_session.execute(stmt)

        return result.unique().fetchall()

    async def del_more(
        self, session: AsyncSession, id_categories: List[int]
    ) -> bool:
        """
        Удаление нескольких категорий
        :param args:
        :param kwargs:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Осуществление операции "
            f"удаления категории по "
            f"id_categories={id_categories}"
        )
        for id_cat in id_categories:
            delete_category = delete(Category).where(Category.id == id_cat)
            await session.execute((delete_category))
            await session.commit()

        return True
