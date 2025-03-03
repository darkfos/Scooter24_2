# Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Type, Sequence

# Local
from database.models.vacancies import Vacancies
from database.repository.general_repository import GeneralSQLRepository


class VacanciesRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Vacancies] = Vacancies
        super().__init__(session=session, model=self.model)

    async def find_all_with_tp_worker(self) -> Sequence[Vacancies]:
        """
        Поиск всех вакансий с информацией о типе рабочего
        :return:
        """

        stmt = select(Vacancies).options(joinedload(Vacancies.type_work))

        result = (await self.async_session.execute(stmt)).scalars().all()
        return result
