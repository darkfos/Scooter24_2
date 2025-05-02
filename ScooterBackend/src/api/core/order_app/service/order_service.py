# System
from typing import List, Union, Type
import logging as logger

import yoomoney
from starlette.responses import RedirectResponse
from yoomoney import Quickpay, Client
import uuid

# Local
from src.database.models.order import Order
from src.database.models.category import Category
from src.api.core.order_app.error.http_order_exception import OrderHttpError
from src.api.core.order_app.schemas.order_dto import (
    OrderAndUserInformation,
    ListOrderAndUserInformation,
    AddOrder, BuyOrder,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository
from src.database.models.order_products import OrderProducts
from src.other.enums.auth_enum import AuthenticationEnum
from src.database.models.enums.order_enum import OrderTypeOperationsEnum
from src.settings.engine_settings import Settings


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

            # Создание отзыва
            is_created: bool = await engine.order_repository.add_one(
                data=Order(
                    date_buy=new_order.date_create,
                    id_user=int(token_data.get("sub")),
                    type_operation=OrderTypeOperationsEnum.NO_BUY,
                    price_result=0,
                )
            )

            if is_created:
                for product in new_order.id_products:
                    # Создание товара в списке заказа
                    create_product_on_list = await engine.order_product_repository.add_one(
                        OrderProducts(
                            id_product=product,
                            id_order=is_created,
                            count_product=0,
                            price=0
                        )
                    )

                    if not create_product_on_list:
                        logging.critical(
                            msg=f"{OrderService.__name__} "
                            f"Не удалось создать новый заказ"
                        )
                        await OrderHttpError().http_failed_to_create_a_new_order()

                return
            await OrderHttpError().http_failed_to_create_a_new_order()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def buy_product(
            engine: IEngineRepository,
            token: str,
            order_buy_data: BuyOrder,
            token_data: dict = dict()
    ) -> None:
        """
        Метод сервиса - осуществление покупки товара
        """

        logging.info(
            msg=f"{OrderService.__name__} "
                f"Осуществление покупки товаров пользователем id={token_data.get('sub')}"
        )

        async with engine:

            price_result: int = 0

            for product in order_buy_data.products:

                # Проверка что количество товаров соответствует имеющемуся
                product_data = await engine.product_repository.find_one(product.id_product)

                if product_data:
                    print(product_data[0], product)
                    if product_data[0].quantity_product >= product.quantity:
                        price_result += (product.price * product.quantity)
                    else:
                        await OrderHttpError().http_order_more_quantity()

            # Удаление старых заказов
            is_deleted = await engine.order_repository.del_more(id_orders=order_buy_data.id_orders)

            label_product = uuid.uuid4()

            if is_deleted:

                # Создание нового заказа
                order_is_created = await engine.order_repository.add_one(
                    data=Order(
                        label_order=label_product,
                        delivery_method=order_buy_data.type_delivery,
                        price_result=price_result,
                        address=order_buy_data.address,
                        telephone_number=order_buy_data.telephone,
                        user_name=order_buy_data.username,
                        email_user=order_buy_data.email,
                        date_buy=order_buy_data.date_create,
                        id_user=int(token_data.get("sub")),
                        type_operation=OrderTypeOperationsEnum.IN_PROCESS,
                    )
                )


                if order_is_created:

                    # Создание списка товаров в заказе

                    for product in order_buy_data.products:

                        product_order_is_created = await engine.order_product_repository.add_one(
                            data=OrderProducts(
                                id_product=product.id_product,
                                id_order=order_is_created,
                                count_product=product.quantity,
                                price=product.price
                            )
                        )

                        if not product_order_is_created:
                            await OrderHttpError().http_failed_to_create_a_new_order()

                    # Создание оплаты
                    url_buy = yoomoney.Quickpay(
                        receiver="4100119127542849",
                        quickpay_form="shop",
                        targets="Покупка товаров с Scooter-24",
                        paymentType="SB",
                        sum=price_result,
                        label=f"{label_product}"
                    )

                    if url_buy:
                        return {
                            "redirect_url": url_buy.base_url
                        }

            await OrderHttpError().http_failed_to_create_a_new_order()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_full_information_by_user_id(
            engine: IEngineRepository,
            token: str,
            token_data: dict = dict(),
            not_buy = False
    ) -> Union[List, List[OrderAndUserInformation]]:
        """
        Метод сервиса для получения всей информации об заказах для пользователя
        :param engine:
        :param token:
        :param token_data:
        :return:
        """

        logging.info(
            msg=f"{OrderService.__name__} "
                f"Получение всей информации о всех заказах для пользователя id={token_data.get('sub')}"
        )

        async with engine:
            # Получаем заказы пользователя с полной информацией
            orders_data: Union[None, List[Order]] = await engine.order_repository.get_full_information(
                id_user=int(token_data.get("sub")),
                not_buy=not_buy
            )

            if orders_data:
                data_orders: list = []

                for order in orders_data:
                    # Собираем товары из заказа
                    products_info = []
                    for order_product in order.product_list:
                        product = order_product.product_data
                        if not product:
                            continue

                        products_info.append({
                            "id_product": product.id,
                            "photos": [photo.read_model() for photo in product.photos] if product.photos else [],
                            "name_product": product.title_product,
                            "price_product": product.price_product,
                            "category_product": product.id_sub_category,
                            "quantity": order_product.count_product
                        })

                    data_orders.append(
                        OrderAndUserInformation(
                            product_data=products_info,
                            order_data={
                                "status": order.type_operation,
                                "price_result": order.price_result,
                                "id_order": order.id,
                                "date_buy": order.date_buy,
                                "email_user": order.email_user,
                                "user_name": order.user_name,
                                "telephone_number": order.telephone_number,
                                "address": order.address,
                                "delivery_method": order.delivery_method,
                            },
                        )
                    )
                return ListOrderAndUserInformation(orders=data_orders)

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
                        "name_product": order_product_data.get(
                            "title_product"
                        ),
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

            print(order_data, id_order, "#"*30)

            if order_data:
                if order_data[0].id_user == int(token_data.get("sub")):

                    # Удаление заказа
                    is_deleted: bool = (
                        await engine.order_repository.delete_one(
                            other_id=int(id_order)
                        )
                    )

                    if is_deleted:
                        # Очистка кэша
                        await redis.delete_key(key=f"orders_by_token_{token}")
                        return
                    await OrderHttpError().http_failed_to_delete_order()
            logging.critical(
                msg=f"{OrderService.__name__} "
                f"Не удалось удалить заказ, "
                f"заказ не был найден"
            )
            await OrderHttpError().http_order_not_found()
