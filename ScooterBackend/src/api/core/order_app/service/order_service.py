from typing import List, Union, Type
import logging as logger

import yoomoney
from starlette.datastructures import FormData
import uuid

from src.database.models.enums.delivery_type_enum import DeliveryMethod
from src.database.models.enums.type_buy_enum import TypeBuy

from src.database.models.order import Order
from src.api.core.order_app.error.http_order_exception import OrderHttpError
from src.api.core.order_app.schemas.order_dto import (
    OrderAndUserInformation,
    ListOrderAndUserInformation,
    AddOrder,
    BuyOrder,
    OrderIsBuy,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository
from src.database.models.order_products import OrderProducts
from src.other.enums.auth_enum import AuthenticationEnum
from src.database.models.enums.order_enum import OrderTypeOperationsEnum
from src.other.broker.producer.producer import send_transaction_operation

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

            user_orders = (
                await engine.user_repository.find_user_and_get_orders(
                    int(token_data["sub"])
                )
            )

            if user_orders:
                for orderData in user_orders:
                    for product in orderData[0].product_list:
                        if product.id_product in new_order.id_products:
                            await OrderHttpError().http_failed_to_create_a_new_order()

            is_created: bool = await engine.order_repository.add_one(
                data=Order(
                    date_buy=new_order.date_create,
                    id_user=int(token_data.get("sub")),
                    type_operation=OrderTypeOperationsEnum.NO_BUY,
                    type_buy=TypeBuy.CARD,
                    price_result=0,
                )
            )

            if is_created:
                for product in new_order.id_products:
                    create_product_on_list = (
                        await engine.order_product_repository.add_one(
                            OrderProducts(
                                id_product=product,
                                id_order=is_created,
                                count_product=0,
                                price=0,
                            )
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

    @staticmethod
    async def get_order(
        engine: IEngineRepository, id_order: int
    ) -> OrderIsBuy | None:

        if not isinstance(id_order, int):
            await OrderHttpError().http_order_not_found()

        async with engine:
            order_data = await engine.order_repository.check_is_buy(
                id_order=id_order
            )

            if order_data is None:
                await OrderHttpError().http_order_not_found()

            return OrderIsBuy(is_buy=order_data)

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def buy_product(
        engine: IEngineRepository,
        token: str,
        bt: send_transaction_operation,
        order_buy_data: BuyOrder,
        token_data: dict = dict(),
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

                product_data = await engine.product_repository.find_one(
                    product.id_product
                )

                if product_data:
                    if product_data[0].quantity_product >= product.quantity:
                        price_result += (
                            (product.price * product.quantity)
                            * product_data[0].product_discount
                        ) / 100
                    else:
                        await OrderHttpError().http_order_more_quantity()

            is_deleted = await engine.order_repository.del_more(
                id_orders=order_buy_data.id_orders
            )

            label_product = uuid.uuid4()

            if is_deleted:

                type_delivery_product = None

                match order_buy_data.type_delivery:
                    case "pickup":
                        type_delivery_product = DeliveryMethod.PICKUP
                    case "standard":
                        type_delivery_product = DeliveryMethod.STANDARD
                    case "express":
                        type_delivery_product = DeliveryMethod.EXPRESS

                # Создание нового заказа
                order_is_created = await engine.order_repository.add_one(
                    data=Order(
                        label_order=label_product,
                        delivery_method=type_delivery_product,
                        price_result=price_result,
                        address=order_buy_data.address,
                        telephone_number=order_buy_data.telephone,
                        user_name=order_buy_data.username,
                        email_user=order_buy_data.email,
                        date_buy=order_buy_data.date_create,
                        id_user=int(token_data.get("sub")),
                        type_operation=OrderTypeOperationsEnum.IN_PROCESS,
                        type_buy=TypeBuy.CARD,
                    )
                )

                if order_is_created:

                    for product in order_buy_data.products:

                        product_order_is_created = (
                            await engine.order_product_repository.add_one(
                                data=OrderProducts(
                                    id_product=product.id_product,
                                    id_order=order_is_created,
                                    count_product=product.quantity,
                                    price=product.price,
                                )
                            )
                        )

                        if not product_order_is_created:
                            await OrderHttpError().http_failed_to_create_a_new_order()

                    url_buy = yoomoney.Quickpay(
                        receiver="4100119127542849",
                        quickpay_form="shop",
                        targets="Покупка товаров с Scooter-24",
                        paymentType="SB",
                        sum=price_result + order_buy_data.price_delivery,
                        label=f"{label_product}",
                    )

                    create_product_data = await engine.order_repository.get_all_product_list_on_id(
                        _id=order_is_created
                    )

                    await bt(order_data=create_product_data)

                    if url_buy:
                        return {"redirect_url": url_buy.base_url}

            await OrderHttpError().http_failed_to_create_a_new_order()

    @staticmethod
    async def notification_order(
        engine: IEngineRepository, data_order: FormData
    ) -> None:
        if label := data_order.get("label"):
            async with engine:
                order = await engine.order_repository.find_by_label(label)

                if not order:
                    await OrderHttpError().http_order_not_found()
                    return

                order.type_operation = OrderTypeOperationsEnum.SUCCESS
                order.transaction_id = data_order.get("operation_id")

                for op in order.product_list:
                    if product := (
                        await engine.product_repository.find_one(op.id_product)
                    )[0]:
                        product.quantity_product = max(
                            0, product.quantity_product - op.count_product
                        )

                        isupdated = await engine.product_repository.update_one(
                            op.id_product,
                            {"quantity_product": product.quantity_product},
                        )

                        if not isupdated:
                            await OrderHttpError().http_failed_to_create_a_new_order()

                await engine.order_repository.update_one(
                    order.id,
                    {
                        "type_operation": OrderTypeOperationsEnum.SUCCESS,
                        "transaction_id": data_order.get("operation_id"),
                    },
                )
                return

        await OrderHttpError().http_order_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_full_information_by_user_id(
        engine: IEngineRepository,
        token: str,
        token_data: dict = dict(),
        not_buy=False,
    ) -> ListOrderAndUserInformation | None:
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
            orders_data: Union[None, List[Order]] = (
                await engine.order_repository.get_full_information(
                    id_user=int(token_data.get("sub")), not_buy=not_buy
                )
            )

            if orders_data:
                data_orders: list = []

                for order in orders_data:
                    products_info = []
                    for order_product in order.product_list:
                        product = order_product.product_data
                        if not product:
                            continue

                        products_info.append(
                            {
                                "id_product": product.id,
                                "photos": (
                                    [
                                        photo.read_model()
                                        for photo in product.photos
                                    ]
                                    if product.photos
                                    else []
                                ),
                                "name_product": product.title_product,
                                "price_product": product.price_product,
                                "category_product": product.id_sub_category,
                                "quantity": order_product.count_product,
                            }
                        )

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
    ) -> OrderAndUserInformation | None:
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
                products_info = []

                for order_product in order_data[0].product_list:
                    product = order_product.product_data
                    if not product:
                        continue

                    products_info.append(
                        {
                            "id_product": product.id,
                            "photos": (
                                [
                                    photo.read_model()
                                    for photo in product.photos
                                ]
                                if product.photos
                                else []
                            ),
                            "name_product": product.title_product,
                            "price_product": product.price_product,
                            "category_product": product.id_sub_category,
                            "quantity": order_product.count_product,
                        }
                    )

                return OrderAndUserInformation(
                    product_data=products_info,
                    order_data={
                        "status": order_data[0].type_operation,
                        "price_result": order_data[0].price_result,
                        "id_order": order_data[0].id,
                        "date_buy": order_data[0].date_buy,
                        "email_user": order_data[0].email_user,
                        "user_name": order_data[0].user_name,
                        "telephone_number": order_data[0].telephone_number,
                        "address": order_data[0].address,
                        "delivery_method": order_data[0].delivery_method,
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
            order_data: Union[None, Order] = (
                await engine.order_repository.find_one(other_id=id_order)
            )

            if order_data:
                if order_data[0].id_user == int(token_data.get("sub")):

                    is_deleted: bool = (
                        await engine.order_repository.delete_one(
                            other_id=int(id_order)
                        )
                    )

                    if is_deleted:
                        await redis.delete_key(key=f"orders_by_token_{token}")
                        return
                    await OrderHttpError().http_failed_to_delete_order()
            logging.critical(
                msg=f"{OrderService.__name__} "
                f"Не удалось удалить заказ, "
                f"заказ не был найден"
            )
            await OrderHttpError().http_order_not_found()
