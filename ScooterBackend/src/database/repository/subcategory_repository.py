from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.subcategory import SubCategory
from typing import Union, List
from sqlalchemy import select, Result


class SubCategoryRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession, model=None):
        super().__init__(session, SubCategory)

    async def find_by_name(
            self,
            name_subcategory
    ) -> Union[None, SubCategory]:
        sub_category_data = select(SubCategory).where(
            SubCategory.name == name_subcategory
        )
        sub_category_data: Result = await  \
            self.async_session.execute(sub_category_data)

        if sub_category_data:
            return sub_category_data.fetchone()
        return None

    async def find_subcategories_by_id_category(
            self,
            id_category: int
    ) -> List[SubCategory]:
        stmt = select(SubCategory).where(SubCategory.id_category == id_category)
        result = (await self.async_session.execute(stmt)).fetchall()
        return result
