# Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type

# Local
from src.database.models.vacancy_request import VacancyRequest
from src.database.repository.general_repository import GeneralSQLRepository


class VacanciesRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[VacancyRequest] = VacancyRequest
        super().__init__(session=session, model=self.model)
