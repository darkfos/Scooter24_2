from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.sub_sub_category import SubSubCategory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class SubSubCategoryRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=SubSubCategory)

    async def find_all_s_subcategory_by_id_s(
        self, id_s: int
    ) -> List[SubSubCategory]:

        stmt = select(SubSubCategory).where(
            SubSubCategory.id_sub_category == id_s
        )
        result = (await self.async_session.execute(stmt)).fetchall()
        return result
