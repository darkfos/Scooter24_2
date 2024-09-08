#System
from typing import List, Union, Type

#Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, Result
from sqlalchemy.orm import joinedload

#Local
from src.database.models.order import Order
from src.database.repository.general_repository import GeneralSQLRepository


class OrderRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Order = Order
        super().__init__(session=session, model=self.model)

    async def del_more(self, id_orders: List[int]) -> bool:
        """
        Удаление нескольких заказов
        :param args:
        :param kwargs:
        :return:
        """

        for id_order in id_orders:
            del_order = delete(Order).where(Order.id == id_order)
            await self.async_session.execute(del_order)
            await self.async_session.commit()

        return True

    async def get_full_information(self, id_user: int = None, id_order: int = None, type_find: Union[str, None] = None) -> Union[List, List[Order], None]:
        """
        Получение всех заказов + подробная информация по id пользователя.
        :param id_user:
        :return:
        """

        if id_user:
            stmt = select(Order).where(Order.id_user == id_user).options(
                joinedload(Order.ord_user),
                joinedload(Order.product_info)
            )
        else:
            stmt = select(Order).where(Order.id == id_order).options(
                joinedload(Order.ord_user),
                joinedload(Order.product_info)
            )

        if type_find:
            orders_data = ((await self.async_session.execute(stmt)).unique()).one_or_none()
            return orders_data
        else:
            orders_data = ((await self.async_session.execute(stmt)).unique()).fetchall()

            if orders_data:
                return orders_data[0]
            return []