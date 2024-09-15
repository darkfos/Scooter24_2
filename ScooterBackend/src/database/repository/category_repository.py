#System
from typing import Union, List, Type

#Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result
from sqlalchemy import select, update, delete

#Local
from src.database.models.category import Category
from src.database.db_worker import db_work
from src.database.repository.general_repository import GeneralSQLRepository


class CategoryRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Category] = Category
        super().__init__(session=session, model=self.model)

    async def find_by_name(self, category_name: str, type_find: bool = False) -> bool:
        """
        Поиск категории по названию
        :param category_name:
        :return:
        """

        stmt = select(Category).where(Category.name_category == category_name)
        res_to_find = (await self.async_session.execute(stmt)).one_or_none()

        if type_find:
            return res_to_find[0]

        if res_to_find:
            return True
        return False

    async def del_more(session: AsyncSession, id_categories: List[int]) -> bool:
        """
        Удаление нескольких категорий
        :param args:
        :param kwargs:
        :return:
        """

        for id_cat in id_categories:
            delete_category = delete(Category).where(Category.id == id_cat)
            await session.execute((delete_category))
            await session.commit()

        return True