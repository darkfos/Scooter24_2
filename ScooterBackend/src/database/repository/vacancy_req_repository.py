# Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type

# Local
from database.models.vacancy_request import VacancyRequest
from database.repository.general_repository import GeneralSQLRepository


class VacanciesReqRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[VacancyRequest] = VacancyRequest
        super().__init__(session=session, model=self.model)
