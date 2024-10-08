# Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.type_worker import TypeWorker
from typing import Type


class TypeWorkerRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[TypeWorker] = TypeWorker
        super().__init__(session=session, model=self.model)
