from src.database.repository.general_repository import GeneralSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.model import Model


class ModelRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Model)