# System
from typing import Annotated

# Other libraries
from fastapi import Depends, status, APIRouter


# Local
from src.api.authentication.secure.authentication_service import Authentication
from src.database.db_worker import db_work
from src.api.core.history_catalog.schemas.history_buy_dto import *
from src.api.core.history_catalog.service.history_buy_service import HistoryBuyService
from src.api.dep.dependencies import IEngineRepository, EngineRepository


auth: Authentication = Authentication()
history_buy_router: APIRouter = APIRouter(
    prefix="/history_buy", tags=["History buy - Истории покупок товаров"]
)


@history_buy_router.post(
    path="/create_new_history",
    description="""
    ### Endpoint - создание новой истории.
    Данный метод позволяет создать новую историю покупки товара.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Создание истории",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def create_new_history(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    new_history: HistoryBuyBase,
) -> None:
    """
    ENDPOINT - Создание новой истории
    :param session:
    :param user_data:
    :param new_history:
    :return:
    """

    return await HistoryBuyService.create_history(
        engine=session,
        token=user_data,
        new_history=new_history,
    )


@history_buy_router.get(
    path="/get_all_history_for_user",
    description="""
    ### Endpoint - Получение всей истории покупок пользователя.
    Данный метод позволяет пользователю узнать всю свою историю покупок.
    Необходим jwt ключ и Bearer в заголовке
    """,
    summary="Полная история покупок",
    status_code=status.HTTP_200_OK,
    response_model=Union[List, List[HistoryBuyBase]],
)
async def get_all_histories_for_user(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)],
) -> Union[List, List[HistoryBuyBase]]:
    """
    ENDPOINT - Получение списка истории всех покупок пользователя
    :param session:
    :param user_data:
    :return:
    """

    return await HistoryBuyService.get_all_histories_for_user(
        engine=session, token=user_data
    )


@history_buy_router.get(
    path="/get_history_by_id/{id_history}",
    description="""
    ### Endpoint - Получение данных об истории.
    Данный метод позволяет получить данные об истории по id.
    Необходимо передать id истории в ссылку запроса.
    Необходим jwt ключ и Bearer в заголовке.
    """,
    status_code=status.HTTP_200_OK,
    response_model=HistoryBuyBase,
)
async def get_data_about_history_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    id_history: int,
) -> HistoryBuyBase:
    """
    ENDPOINT - Поиск истории по id
    :param session:
    :param user_data:
    :return:
    """

    return await HistoryBuyService.get_history_by_id(
        engine=session, token=user_data, id_history=id_history
    )


@history_buy_router.delete(
    path="/delete_history_by_id/{id_history}",
    description="""
    ### Endpoint - Удаление истории по id.
    Данный метод позволяет удалить историю по id.
    Удалить может только администратор!
    Необходимо передать jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Удаление истории",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    tags=["AdminPanel - Панель администратора"],
)
async def delete_history_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_history: int,
) -> None:
    """
    ENDPOINT - Удаление истории по id
    :param session:
    :param admin_data:
    :param id_history:
    :return:
    """

    return await HistoryBuyService.delete_history_by_id(
        engine=session, token=admin_data, id_history=id_history
    )
