# System
from typing import List, Union, Type
import logging as logger

# Local
from src.database.models.order import Order
from src.database.models.category import Category
from src.api.core.order_catalog.error.http_order_exception import OrderHttpError
from src.api.core.order_catalog.schemas.order_dto import (
    OrderAndUserInformation,
    ListOrderAndUserInformation,
    AddOrder,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum
from src.database.models.enums.order_enum import OrderTypeOperationsEnum


# Redis
from src.store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class OrderService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_new_order(
        engine: IEngineRepository,
        token: str,
        new_order: AddOrder,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для создания нового заказа
        :param session:
        :param token:
        :param new_review:
        :return:
        """

        logging.info(msg=f"{OrderService.__name__} Создание нового заказа")

        async with engine:
            # Данные продукта
            product_data = await engine.product_repository.find_one(new_order.id_product)

            print(product_data)

            # Создание отзыва
            is_created: bool = await engine.order_repository.add_one(
                data=Order(
                    date_buy=new_order.date_create,
                    id_user=token_data.get("sub"),
                    id_product=new_order.id_product,
                    count_product = 0,
                    type_operation =  OrderTypeOperationsEnum.NO_BUY,
                    price_result=product_data[0].price_product
                )
            )

            if is_created:
                return
            logging.critical(
                msg=f"{OrderService.__name__} "
                f"Не удалось создать новый заказ"
            )
            await OrderHttpError().http_failed_to_create_a_new_order()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_full_information_by_user_id(
        engine: IEngineRepository,
        token: str,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> Union[List, List[OrderAndUserInformation]]:
        """
        Метод сервиса для получения всей информации об заказах для пользователя
        :param session:
        :param id_user:
        :return:
        """

        logging.info(
            msg=f"{OrderService.__name__} "
            f"Получение всей информации о всех заказах"
        )

        async with engine:
            # Данные заказов пользователя
            orders_data: Union[None, List[Order]] = (
                await engine.order_repository.get_full_information(
                    id_user=token_data.get("sub")
                )
            )

            if orders_data:
                data_orders: list = []
                for order in orders_data:
                    order_product_data: dict = order[
                        0
                    ].product_info.read_model()
                    get_category: Union[None, Category] = (
                        await engine.subcategory_repository.find_one(
                            other_id=order_product_data.get("id_sub_category")
                        )
                    )

                    data_orders.append(
                        OrderAndUserInformation(
                            product_data={
                                "name_product": order_product_data.get(
                                    "title_product"
                                ),
                                "price_product": order_product_data.get(
                                    "price_product"
                                ),
                                "category_product": (
                                    get_category[0].name
                                    if get_category
                                    else None
                                ),  # noqa
                            },
                            order_data={
                                "status": order[0].type_operation,
                                "quantity": order[0].count_product,
                                "price_result": order[0].price_result,
                                "id_order": order[0].id,
                                "date_buy": order[0].date_buy,
                            },
                        )
                    )
                return ListOrderAndUserInformation(orders=[*data_orders])

            return ListOrderAndUserInformation(orders=[])

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_information_about_order_by_id(
        engine: IEngineRepository,
        token: str,
        id_order: int,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> OrderAndUserInformation:
        """
        Метод сервиса для получения полной информации о заказе по id
        :param session:
        :param token:
        :param id_order:
        :return:
        """

        logging.info(
            msg=f"{OrderService.__name__} "
            f"Получение полной информации о "
            f"заказе id_order={id_order}"
        )

        async with engine:
            # Получение данных заказа
            order_data: Union[None, Order] = (
                await engine.order_repository.get_full_information(
                    id_order=id_order
                )
            )

            if order_data:
                order_user_data: dict = order_data[0].ord_user.read_model()
                order_product_data: dict = order_data[
                    0
                ].product_info.read_model()  # noqa
                get_category: Union[None, Category] = (
                    await engine.order_repository.find_one(
                        other_id=order_product_data.get("id_category")
                    )
                )
                return OrderAndUserInformation(
                    product_data={
                        "name_product": order_product_data.get("title_product"),
                        "price_product": order_product_data.get(
                            "price_product"
                        ),  # noqa
                        "category_product": (
                            get_category[0].name_category
                            if get_category
                            else ""
                        ),  # noqa
                        "date_buy": order_data[0].date_buy,
                    },
                    user_data={
                        "user_name": order_user_data.get("name_user"),
                        "surname_user": order_user_data.get("surname_user"),
                        "email": order_user_data.get("email_user"),
                    },
                )
            logging.critical(
                msg=f"{OrderService.__name__} "
                f"Не удалось получить информацию о заказе,"
                f" заказ не был найден"
            )
            await OrderHttpError().http_order_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_order_by_id(
        engine: IEngineRepository,
        token: str,
        id_order: int,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для удаления заказа по id
        :param session:
        :param token:
        :param id_order:
        :return:
        """

        logging.info(
            msg=f"{OrderService.__name__} "
            f"Удаление заказа по id_order={id_order}"
        )

        async with engine:
            # Проверка на то что заказ принадлежит покупателю
            order_data: Union[None, Order] = (
                await engine.order_repository.find_one(other_id=id_order)
            )

            if order_data:
                if order_data[0].id_user == token_data.get("id_user"):

                    # Удаление заказа
                    is_deleted: bool = await engine.order_repository.delete_one(
                        other_id=id_order
                    )

                    if is_deleted:
                        return
                    await OrderHttpError().http_failed_to_delete_order()
            logging.critical(
                msg=f"{OrderService.__name__} "
                f"Не удалось удалить заказ, "
                f"заказ не был найден"
            )
            await OrderHttpError().http_order_not_found()
