from src.database.models.brand import Brand
from src.database.repository.general_repository import GeneralSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession


class BrandRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Brand)
