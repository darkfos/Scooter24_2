from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload


# Local
from database.repository.general_repository import (
    GeneralSQLRepository,
)  # noqa
from database.models.garage import Garage


class GarageRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Garage)

    async def all_by_id_user(self, id_user: int):
        """
        Получение всех транспортов с гаража
        :param id_user:
        :return:
        """

        stmt = (
            select(Garage)
            .options(
                joinedload(Garage.mark_data),
                joinedload(Garage.model_data),
                joinedload(Garage.type_moto_data),
            )
            .where(Garage.id_user == id_user)
        )
        result = await self.async_session.execute(stmt)
        return result.unique().all()

    async def delete_user_mt(self, id_user: int, id_mt: int) -> None:
        """
        Удаление транспорта из гаража по id_user && id_mt
        :param id_mt:
        :param id_user:
        :return:
        """

        stmt = delete(Garage).where(
            Garage.id_user == id_user, Garage.id == id_mt
        )
        result = await self.async_session.execute(stmt)
        await self.async_session.commit()
        return result.rowcount
