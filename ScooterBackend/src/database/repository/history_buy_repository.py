# System
from typing import Union, List, Type
import logging

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, Result

# Local
from src.database.models.history_buy import HistoryBuy
from src.database.repository.general_repository import GeneralSQLRepository


class HistoryBuyRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[HistoryBuy] = HistoryBuy
        super().__init__(session=session, model=self.model)

    async def del_more(self, id_histories: List[int]) -> bool:
        """
        Удаление нескольких записей об покупке товара
        :param args:
        :param kwargs:
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} Удаление нескольких записей об покупке товара id = {id_histories}")
        for id_history in id_histories:
            delete_history: Result = delete(HistoryBuy).where(
                HistoryBuy.id == id_history
            )
            await self.async_session.execute(delete_history)
            await self.async_session.commit()

        return True

    async def find_by_user_id(self, id_user: int) -> Union[List, List[HistoryBuy]]:
        """
        Получение истории покупок
        :param id_user:
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} Поиск пользователя по id = {id_user}")
        stmt = select(HistoryBuy).where(HistoryBuy.id_user == id_user)
        all_history = (await self.async_session.execute(stmt)).all()

        if all_history:
            return all_history[0]
        return []
