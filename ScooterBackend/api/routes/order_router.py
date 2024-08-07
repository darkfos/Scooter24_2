#System
from typing import Annotated

#Other libraries
from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from api.authentication.authentication_service import Authentication
from database.db_worker import db_work
from api.dto.order_dto import *
from api.service.order_service import OrderService
from api.dep.dependencies import IEngineRepository, EngineRepository


auth: Authentication = Authentication()
order_router: APIRouter = APIRouter(
    prefix="/order",
    tags=["Order - Заказы пользователей"]
)


@order_router.post(
    path="/create_order",
    description="""
    ### Endpoint - Создание заказа.
    Данный метод позволяет создать заказ.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Создание заказа",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def create_a_new_order(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    new_order: AddOrder
) -> None:
    """
    ENDPOINT - Добавление нового заказа
    :param session:
    :param usr_data:
    :param new_order:
    :return:
    """

    return await OrderService.create_new_order(engine=session, token=user_data, new_order=new_order)


@order_router.get(
    path="/get_orders_by_id_user",
    description="""
    ### Endpoint - Получение всех заказов пользователя.
    Данный метод позволяет получить все заказы пользователя.
    Необходимо передать id пользователя.
    """,
    summary="Все заказы пользователя",
    response_model=Union[List, List[OrderAndUserInformation]],
    status_code=status.HTTP_200_OK
)
async def get_orders_by_id_user(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)]
) -> Union[List, List[OrderAndUserInformation]]:
    """
    ENDPOINT - Получение всех заказов пользователя, подробная информация
    :param session:
    :param id_user:
    :return:
    """

    return await OrderService.get_full_information_by_user_id(engine=session, token=user_data)


@order_router.get(
    path="/get_order_by_id/{id_order}",
    description="""
    ### Endpoint - Получение полной информации о заказе по id.
    Данный метод позволяет получить полную информацию о заказе по id.
    """,
    summary="Информация о заказе",
    status_code=status.HTTP_200_OK,
    response_model=OrderAndUserInformation
)
async def get_information_about_order_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    id_order: int
) -> OrderAndUserInformation:
    """
    ENDPOINT - Получение информации о заказе по id заказа
    :param session:
    :param user_data:
    :param id_order:
    :return:
    """

    return await OrderService.get_information_about_order_by_id(
        engine=session, token=user_data, id_order=id_order
    )


@order_router.delete(
    path="/delete_order/{id_order}",
    description="""
    ### Endpoint - Удаление заказа по id.
    Данный метод позволяет удалить заказ по id.
    Необходимо в ссылке передать id заказа.
    Необходим jwt ключ и Bearer в заголовке.
    """,
    summary="Удаление заказа",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_order_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    id_order: int
) -> None:
    """
    ENDPOINT - Удаление заказа по id
    :param session:
    :param user_data:
    :param id_order:
    :return:
    """

    return await OrderService.delete_order_by_id(engine=session, token=user_data, id_order=id_order)