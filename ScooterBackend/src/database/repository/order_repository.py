# System
from typing import List, Union, Type, Sequence
import logging as logger

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, Row, desc, and_
from sqlalchemy.orm import joinedload

# Local
from src.database.models.order import Order
from src.database.models.order_products import OrderProducts
from src.database.models.product import Product
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.enums.order_enum import OrderTypeOperationsEnum


logging = logger.getLogger(__name__)


class OrderRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Order] = Order
        super().__init__(session=session, model=self.model)

    async def find_by_label(self, label: str) -> Sequence[Row]:
        """
        Поиск заказа по метке
        """

        stmt = select(Order).where(Order.label_order == label).options(
            joinedload(Order.product_list)
        )
        result = await self.async_session.execute(stmt)
        return result.unique().scalars().first()

    async def get_last_products(self) -> Sequence[Row]:
        """
        Последние проданные товары
        :return:
        """

        stmt = (
            select(Order)
            .options(
                joinedload(Order.product_list).joinedload(OrderProducts.product_data),
                joinedload(Order.product_list).joinedload(OrderProducts.product_data).joinedload(
                    Product.product_models_data
                ),
                joinedload(Order.product_list).joinedload(OrderProducts.product_data).joinedload(
                    Product.photos
                ),
                joinedload(Order.product_list).joinedload(OrderProducts.product_data).joinedload(
                    Product.brand_mark
                ),
                joinedload(Order.product_list).joinedload(OrderProducts.product_data).joinedload(
                    Product.type_models
                ),
            )
            .where(Order.type_operation == OrderTypeOperationsEnum.SUCCESS)
            .order_by(desc(Order.date_buy))
            .limit(7)
        )
        result = await self.async_session.execute(stmt)
        return result.unique().all()

    async def del_more(self, id_orders: List[int]) -> bool:
        """
        Удаление нескольких заказов
        :param id_orders:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Удаление нескольких"
            f" заказов id = {id_orders}"
        )
        del_order = delete(Order).where(Order.id.in_(id_orders))
        await self.async_session.execute(del_order)
        await self.async_session.commit()

        return True

    async def get_full_information(
        self,
        id_user: int = None,
        id_order: int = None,
        type_find: Union[str, None] = None,
        not_buy: bool = False
    ) -> Union[List, List[Order], None]:
        """
        Получение всех заказов + подробная
        информация по id пользователя или по id заказа.
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
                f"Получение полной информации "
                f"по id_user = {id_user}, id_order = {id_order}"
        )

        if id_user:
            conditions = [Order.id_user == id_user]
            if not_buy:
                conditions.append(
                    Order.type_operation.in_(
                        [
                            OrderTypeOperationsEnum.NO_BUY,
                            OrderTypeOperationsEnum.IN_PROCESS
                        ]
                    )
                )
            stmt = (
                select(Order)
                .where(and_(*conditions))
                .options(
                    joinedload(Order.ord_user),
                    joinedload(Order.product_list)
                        .joinedload(OrderProducts.product_data)
                        .joinedload(Product.photos),
                )
            )
        elif id_order:
            stmt = (
                select(Order)
                .where(Order.id == id_order)
                .options(
                    joinedload(Order.ord_user),
                    joinedload(Order.product_list)
                        .joinedload(OrderProducts.product_data)
                        .joinedload(Product.photos),
                )
            )
        else:
            # Если не переданы id_user и id_order, возвращаем пустой список
            return []

        result = await self.async_session.execute(stmt)

        if type_find:
            order = result.unique().one_or_none()
            return order
        else:
            orders = result.unique().scalars().all()
            return orders if orders else []