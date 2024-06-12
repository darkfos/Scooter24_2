#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.database.models.vacancies import Vacancies
from ScooterBackend.database.repository.general_repository import GeneralSQLRepository


class VacanciesRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model = Vacancies
        super().__init__(
            session=session,
            model=self.model
        )