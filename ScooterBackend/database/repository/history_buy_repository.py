#System
from typing import Union, List, Type

#Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, Result

#Local
from database.models.history_buy import HistoryBuy
from database.repository.general_repository import GeneralSQLRepository


class HistoryBuyRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: HistoryBuy = HistoryBuy
        super().__init__(session=session, model=self.model)

    async def del_more(self, id_histories: List[int]) -> bool:
        """
        Удаление нескольких записей об покупке товара
        :param args:
        :param kwargs:
        :return:
        """

        for id_history in id_histories:
            delete_history: Result = delete(HistoryBuy).where(HistoryBuy.id == id_history)
            await self.async_session.execute(delete_history)
            await self.async_session.commit()

        return True

    async def find_by_user_id(self, id_user: int) -> Union[List, List[HistoryBuy]]:
        """
        Получение истории покупок
        :param id_user:
        :return:
        """

        stmt = select(HistoryBuy).where(HistoryBuy.id_user == id_user)
        all_history = (await self.async_session.execute(stmt)).all()

        if all_history:
            return all_history[0]
        return []