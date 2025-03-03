from database.models.product_marks import ProductMarks
from database.repository.general_repository import GeneralSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ProductMarksRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=ProductMarks)
