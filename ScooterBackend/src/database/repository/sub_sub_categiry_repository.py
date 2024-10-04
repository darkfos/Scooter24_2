from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.sub_sub_category import SubSubCategory
from sqlalchemy.ext.asyncio import AsyncSession


class SubSubCategoryRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=SubSubCategory)