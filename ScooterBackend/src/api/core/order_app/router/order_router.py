from typing import Annotated, Type
import logging

from fastapi import Depends, status, APIRouter, Request

from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.order_app.schemas.order_dto import (
    OrderAndUserInformation,
    AddOrder,
    BuyOrder,
    ListOrderAndUserInformation,
    OrderIsBuy,
)
from src.api.core.order_app.service.order_service import OrderService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from src.other.broker.producer.producer import send_transaction_operation


auth: Authentication = Authentication()
order_router: APIRouter = APIRouter(
    prefix=APIPrefix.ORDER_PREFIX.value, tags=[APITagsEnum.ORDER.value]
)
logger: Type[logging.Logger] = logging.getLogger(__name__)


@order_router.post(
    path="/notification",
    description="""
    ### ENDPOINT - Получение уведомления с платежного сервиса
    """,
    summary="Подверждение покупки товара",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def success_order(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    request: Request,
):
    data = await request.form()

    await OrderService.notification_order(data_order=data, engine=session)


@order_router.post(
    path="/create",
    description="""
    ### Endpoint - Создание заказа.
    Данный метод позволяет создать заказ.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Создание заказа",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def create_a_new_order(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    new_order: AddOrder,
) -> None:
    """
    ENDPOINT - Добавление нового заказа
    :param session:
    :param usr_data:
    :param new_order:
    :return:
    """

    logger.info(
        msg="Order-Router вызов метода " "создания заказа (create_order)"
    )

    return await OrderService.create_new_order(
        engine=session, token=user_data, new_order=new_order
    )


@order_router.post(
    path="/buy",
    description="""
    ### ENDPOINT - Покупка товара пользователем
    Доступен авторизированым пользователям
    """,
    summary="Покупка товара",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def buy_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    order_data: BuyOrder,
) -> dict:
    """
    Покупка товара пользователем
    """

    logger.info(msg="Order-Router покупка пользователем товара")

    resultBuyProduct = await OrderService.buy_product(
        engine=session,
        token=user_data,
        order_buy_data=order_data,
        bt=send_transaction_operation,
    )

    return resultBuyProduct


@order_router.get(
    path="/all/user",
    description="""
    ### Endpoint - Получение всех заказов пользователя.
    Данный метод позволяет получить все заказы пользователя.
    Необходимо передать id пользователя.
    """,
    summary="Все заказы пользователя",
    response_model=ListOrderAndUserInformation,
    status_code=status.HTTP_200_OK,
)
async def get_orders_by_id_user(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    not_buy: bool = True,
) -> ListOrderAndUserInformation:
    """
    ENDPOINT - Получение всех заказов пользователя,
    подробная информация
    :param session:
    :param id_user:
    :return:
    """

    logger.info(
        msg="Order-Router вызов метода "
        "получения заказов по "
        "id пользователя (get_orders_by_id_user)"
    )

    return await OrderService.get_full_information_by_user_id(
        engine=session, token=user_data, not_buy=not_buy
    )


@order_router.get(
    path="/unique/{id_order}",
    description="""
    ### Endpoint - Получение полной информации о заказе по id.
    Данный метод позволяет получить полную информацию о заказе по id.
    """,
    summary="Информация о заказе",
    status_code=status.HTTP_200_OK,
    response_model=OrderAndUserInformation,
)
async def get_information_about_order_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    id_order: int,
) -> OrderAndUserInformation:
    """
    ENDPOINT - Получение информации о заказе по id заказа
    :param session:
    :param user_data:
    :param id_order:
    :return:
    """

    logger.info(
        msg="Order-Router вызов метода получения"
        " информации о заказе по "
        "id заказа (get_information_about_order_by_id)"
    )

    return await OrderService.get_information_about_order_by_id(
        engine=session,
        token=user_data,
        id_order=id_order,
        redis_search_data="order_by_id_%s" % id_order,
    )


@order_router.get(
    path="/check_buy/{id_order}",
    description="""
        ENDPOINT - Получение информации о купленном товаре
    """,
    summary="Уникальный товар, получение информации по покупке",
    status_code=status.HTTP_200_OK,
    response_model=OrderIsBuy,
)
async def unique_check_buy_order(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_order: int,
) -> OrderIsBuy:
    return await OrderService.get_order(engine=engine, id_order=id_order)


@order_router.delete(
    path="/delete/{id_order}",
    description="""
    ### Endpoint - Удаление заказа по id.
    Данный метод позволяет удалить заказ по id.
    Необходимо в ссылке передать id заказа.
    Необходим jwt ключ и Bearer в заголовке.
    """,
    summary="Удаление заказа",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_order_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    id_order: int,
) -> None:
    """
    ENDPOINT - Удаление заказа по id
    :param session:
    :param user_data:
    :param id_order:
    :return:
    """

    logger.info(
        msg="Order-Router вызов метода"
        " удаления заказа по "
        "id (delete_order_by_id)"
    )

    return await OrderService.delete_order_by_id(
        engine=session, token=user_data, id_order=id_order
    )
