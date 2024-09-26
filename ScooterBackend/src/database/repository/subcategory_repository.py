from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.subcategory import SubCategory

class SubCategoryRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession, model=None):
        super().__init__(session, SubCategory)