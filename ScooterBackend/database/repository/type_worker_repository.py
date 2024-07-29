#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from database.repository.general_repository import GeneralSQLRepository
from database.models.type_worker import TypeWorker


class TypeWorkerRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model = TypeWorker
        super().__init__(
            session=session,
            model=self.model
        )