from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.marks import Mark
from sqlalchemy.ext.asyncio import AsyncSession


class MarkRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Mark)
