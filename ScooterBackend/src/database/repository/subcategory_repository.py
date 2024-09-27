from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.subcategory import SubCategory
from typing import Union
from sqlalchemy import select, Result

class SubCategoryRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession, model=None):
        super().__init__(session, SubCategory)

    async def find_by_name(self, name_subcategory) -> Union[None, SubCategory]:
        sub_category_data = select(SubCategory).where(SubCategory.name == name_subcategory)
        sub_category_data: Result = await self.async_session.execute(sub_category_data)
        return sub_category_data.fetchone() if sub_category_data else None