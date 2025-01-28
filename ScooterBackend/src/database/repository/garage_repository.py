from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# Local
from src.database.repository.general_repository import (
    GeneralSQLRepository,
)  # noqa
from src.database.models.garage import Garage


class GarageRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Garage)

    async def all_by_id_user(self, id_user: int):
        """
        Получение всех транспортов с гаража
        :param id_user:
        :return:
        """

        stmt = select(Garage).where(Garage.id_user == id_user)
        result = await self.async_session.execute(stmt)
        return result.all()
