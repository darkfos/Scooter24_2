#System
from typing import List, Dict, Union, Coroutine, Any


#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession


#Local
from src.database.repository.order_repository import OrderRepository
from src.database.repository.category_repository import CategoryRepository
from src.database.models.order import Order
from src.database.models.product import Product
from src.database.models.user import User
from src.database.models.category import Category
from src.api.exception.http_order_exception import OrderHttpError
from src.api.dto.order_dto import *
from src.api.authentication.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository


class OrderService:

    @staticmethod
    async def create_new_order(engine: IEngineRepository, token: str, new_order: AddOrder) -> None:
        """
        Метод сервиса для создания нового заказа
        :param session:
        :param token:
        :param new_review:
        :return:
        """

        #Получение данных с токена
        jwt_data: Coroutine[Any, Any, Dict[str, str] | None] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Создание отзыва
            is_created: bool = await engine.order_repository.add_one(
                data=Order(
                    date_buy=new_order.date_create,
                    id_user=jwt_data.get("id_user"),
                    id_product=new_order.id_product,
                )
            )

            if is_created:
                return

            await OrderHttpError().http_failed_to_create_a_new_order()

    @staticmethod
    async def get_full_information_by_user_id(engine: IEngineRepository, token: str) -> Union[List, List[OrderAndUserInformation]]:
        """
        Метод сервиса для получения всей информации об заказах для пользователя
        :param session:
        :param id_user:
        :return:
        """

        #Получение данных с токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Данные заказов пользователя
            orders_data: Union[None, List[Order]] = await engine.order_repository.get_full_information(id_user=jwt_data.get("id_user"))

            if orders_data:
                data_orders: List[OrderAndUserInformation] = []

                for order in orders_data:
                    order_user_data: dict = order.ord_user.read_model()
                    order_product_data: dict = order.product_info.read_model()
                    get_category: Union[None, Category] = await engine.order_repository.find_one(other_id=order_product_data.get("id_category"))

                    if get_category:
                        data_orders.append(
                            OrderAndUserInformation(
                                product_data={
                                    "name_product": order_product_data.get("title_product"),
                                    "price_product": order_product_data.get("price_product"),
                                    "category_product": get_category[0].name_category,
                                    "date_buy": order.date_buy
                                },
                                user_data={
                                    "user_name": order_user_data.get("name_user"),
                                    "surname_user": order_user_data.get("surname_user"),
                                    "email": order_user_data.get("email_user"),
                                }
                            )
                        )
                    else:
                        continue

                return data_orders

            return []

    @staticmethod
    async def get_information_about_order_by_id(
        engine: IEngineRepository,
        token: str,
        id_order: int
    ) -> OrderAndUserInformation:
        """
        Метод сервиса для получения полной информации о заказе по id
        :param session:
        :param token:
        :param id_order:
        :return:
        """

        #Данные jwt токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Получение данных заказа
            order_data: Union[None, Order] = await engine.order_repository.get_full_information(id_order=id_order)

            if order_data:
                order_user_data: dict = order_data[0].ord_user.read_model()
                order_product_data: dict = order_data[0].product_info.read_model()
                get_category: Union[None, Category] = await engine.order_repository.find_one(
                    other_id=order_product_data.get("id_category"))
                return OrderAndUserInformation(
                    product_data={
                        "name_product": order_product_data.get("title_product"),
                        "price_product": order_product_data.get("price_product"),
                        "category_product": get_category[0].name_category,
                        "date_buy": order_data[0].date_buy
                    },
                    user_data={
                        "user_name": order_user_data.get("name_user"),
                        "surname_user": order_user_data.get("surname_user"),
                        "email": order_user_data.get("email_user")
                    }
                )

            await OrderHttpError().http_order_not_found()

    @staticmethod
    async def delete_order_by_id(engine: IEngineRepository, token: str, id_order: int) -> None:
        """
        Метод сервиса для удаления заказа по id
        :param session:
        :param token:
        :param id_order:
        :return:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на то что заказ принадлежит покупателю
            order_data: Union[None, Order] = await engine.order_repository.find_one(other_id=id_order)

            if order_data:
                if order_data[0].id_user == jwt_data.get("id_user"):

                    #Удаление заказа
                    is_deleted: bool = await engine.order_repository.delete_one(other_id=id_order)

                    if is_deleted:
                        return
                    await OrderHttpError().http_failed_to_delete_order()

            await OrderHttpError().http_order_not_found()