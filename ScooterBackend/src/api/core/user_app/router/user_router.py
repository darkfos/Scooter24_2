from typing import Annotated, Type
import logging

from fastapi import APIRouter, status, Depends

from src.api.authentication.secure.authentication_service import Authentication # noqa
from src.api.core.user_app.schemas.user_dto import (
    InformationAboutUser,
    AllDataUser,
    UserReviewData,
    UserFavouritesData,
    UserIsUpdated,
    DataToUpdate,
    UserIsDeleted,
    BuyingOrders,
)
from src.api.core.user_app.service.user_service import UserService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix

user_router: APIRouter = APIRouter(
    prefix=APIPrefix.USER_PREFIX.value, tags=[APITagsEnum.USER.value]
)
auth: Authentication = Authentication()
logger: Type[logging.Logger] = logging.getLogger(__name__)


@user_router.get(
    path="/information",
    description="""
    ## Endpoint - Краткая информация о пользователе.\n
    Данный метод необходим для получения краткой информации о пользователе.
    В ответе присутсвует лишь информация о пользователе.
    Необходим jwt ключ и Bearer в заголовке Authorization.
    """,
    summary="Краткая информация",
    response_model=InformationAboutUser,
    status_code=status.HTTP_200_OK,
)
async def get_information_about_user(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> InformationAboutUser:
    """
    ENDPOINT - Получение краткой информации о пользователе, (ЛИЧНОЕ)
    :param session:
    :param user_data:
    :return:
    """

    logger.info(
        msg="User-Router вызов метод получения"
        " краткой информации о пользователе (information_about_user)"
    )

    return await UserService.get_information_about_me(
        engine=engine, token=user_data
    )


@user_router.get(
    path="/information/all",
    description="""
    ### Endpoint - Полная информация о пользователе
    Данный метод необходим для получения полной информации о пользователе.\n
    Позволяет узнать следующее:
    1. Заказы пользователя
    2. История заказов
    3. Отзывы
    4. Товары в избранном
    \n
    Необходим jwt ключ и Bearer в заголовке Authorization.
    """,
    summary="Полная информация",
    response_model=AllDataUser,
    status_code=status.HTTP_200_OK,
)
async def get_full_information_about_user(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> AllDataUser:
    """
    ENDPOINT - Получение полной информации об пользователе, (ЛИЧНОЕ
    :param session:
    :return:
    """

    logger.info(
        msg="User-Router вызов метод получения полной"
        " информации о пользователе (full_information_about_user)"
    )

    return await UserService.get_full_information(
        engine=session,
        token=user_data,
        redis_search_data="user_full_information_by_id_%s" % user_data,
    )


@user_router.get(
    path="/all/reviews",
    description="""
    ### Endpoint - Отзывы пользователя.
    Данный метод позволяет получить информацию о
    пользователе, а так же список всех его отзывов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Отзывы пользователя",
    response_model=UserReviewData,
    status_code=status.HTTP_200_OK,
)
async def get_user_data_and_all_reviews(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> UserReviewData:
    """
    ENDPOINT - Получение информации о пользователе + отзывы
    :param session:
    :param user_data:
    :return:
    """

    logger.info(
        msg="User-Router вызов метод получения"
        " всех отзывов пользователя (user_reviews)"
    )

    return await UserService.get_information_about_me_and_review(
        engine=session,
        token=user_data,
        redis_search_data="user_reviews_by_token_%s" % user_data,
    )


@user_router.get(
    path="/all/favourites",
    description="""
    ### Endpoint - Избранные товары пользователя.
    Данный метод позволяет получить информацию о пользователе,
    а так же список избранных товаров. Необходим jwt ключ
    и Bearer в заголовке запроса.
    """,
    summary="Избранное пользователя",
    response_model=UserFavouritesData,
    status_code=status.HTTP_200_OK,
)
async def get_user_data_and_all_favourites_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> UserFavouritesData:
    """
    ENDPOINT - Получение информации о пользователе + избранные товары
    :param session:
    :param user_data:
    :return:
    """

    logger.info(
        msg="User-Router вызов метод получения"
        " всех избранных товаров пользователя (user_favourites)"
    )

    return await UserService.get_information_about_me_and_favourite(
        engine=session,
        token=user_data,
        redis_search_data="user_favourites_by_token_%s" % user_data,
    )


@user_router.get(
    path="/all/orders",
    description="""
    ### Endpoint - Заказы пользователя.
    Данный метод позволяет узнать информацию о пользователе,
     а так же получить список заказов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Заказы пользователя",
    response_model=BuyingOrders,
    status_code=status.HTTP_200_OK,
)
async def get_user_data_and_all_orders(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> BuyingOrders:
    """
    ENDPOINT - Получение информации о пользователе + заказы
    :param session:
    :param user_data:
    :return:
    """

    logger.info(
        msg="User-Router вызов метод получения всех"
        " заказов пользователя (get_user_data_and_all_orders)"
    )

    return await UserService.get_information_about_me_and_orders(
        engine=session,
        token=user_data,
        redis_search_data="user_orders_by_token_%s" % user_data,
    )


@user_router.get(
    path="/success/orders",
    response_model=BuyingOrders,
    status_code=status.HTTP_200_OK,
    description="""
    Получение всех оплаченных пользователем заказов
    """,
    summary="Оплаченные заказы",
)
async def user_success_orders(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> BuyingOrders:
    """
    Оплаченные пользователем заказы
    """

    return await UserService.user_success_orders(
        engine=engine, token=user_data
    )


@user_router.get(
    path="/information/other/{id_user}",
    description="""
    ### Endpoint - Краткая информация о другом пользователе.
    Данный метод позволяет узнать информацию о других пользователях.
    Доступен только для администраторов!
    Необходим jwt ключ и Bearer в заголовке запроса.
    Необходим первичный ключ в ссылке запроса для получения
    данных об указанном пользователе.
    """,
    summary="Другие лица",
    response_model=InformationAboutUser,
    tags=["AdminPanel - Панель администратора"],
)
async def get_information_about_other_users(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_user: int,
) -> InformationAboutUser:
    """
    ENDPOINT - Получение краткой информации о пользователе
    :param session:
    :param id_user:
    :param admin_password:
    :return:
    """

    logger.info(
        msg="User-Router вызов метод получения краткой информации"
        " о другом пользователе по id (get_information_about_other_users)"
    )

    return await UserService.get_information_about_user(
        engine=session,
        user_id=id_user,
        token=admin_data,
        redis_search_data="user_%s" % id_user,
    )


@user_router.get(
    path="/information/all/other/{id_user}",
    description="""
    ### Endpoint - Полная информация о другом пользователе.
    Данный метод позволяет узнать информацию о других пользователях.
    Необходим пароль администратора в заголовке.
    Необходим первичный ключ в ссылке запроса для получения
    данных об указанном пользователе.
    """,
    summary="Полная информация о другом пользователе",
    response_model=AllDataUser,
    status_code=status.HTTP_200_OK,
    tags=["AdminPanel - Панель администратора"],
)
async def get_all_information_about_other_users(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_user: int,
) -> AllDataUser:
    """
    ENDPOINT - Получение полной информации о других пользователях
    :param session:
    :param id_user:
    :param admin_password:
    :return:
    """

    logger.info(
        msg="User-Router вызов метод получение полной информации"
        " о пользователе по id (other_user_all_data)"
    )

    return await UserService.get_full_information_other_user(
        engine=session,
        token=admin_data,
        user_id=id_user,
    )


@user_router.put(
    path="/update",
    description="""
    ### Endpoint - Обновление информации о пользователе.
    Данный метод позволяет обновить информацию о пользователе,
    как всю, так и некоторую.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Обновление данных пользователя",
    response_model=UserIsUpdated,
    status_code=status.HTTP_200_OK,
)
async def update_user_information(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    data_to_update: DataToUpdate,
) -> UserIsUpdated:
    """
    ENDPOINT - Обновление данных о пользователе
    :return:
    """

    logger.info(
        msg="User-Router вызов метод обновления"
        " информации о пользователе (update_user_information)"
    )
    return await UserService.update_user_information(
        engine=session, token=user_data, to_update=data_to_update
    )


@user_router.delete(
    path="/delete",
    description="""
    ### Endpoint - УДАЛЕНИЕ пользователя.
    Удаление пользователя, безвозвратное удаление данных,
    предельная ОСТОРОЖНОСТЬ!
    Для удаления необходим jwt ключ и Bearer в заголовке.
    """,
    summary="Удаление пользователя",
    response_model=UserIsDeleted,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> UserIsDeleted:
    """
    Удаление всех данных о пользователе
    """

    logger.info(
        msg="User-Router вызов метод"
        " удаления пользователя по id (delete_user)"
    )

    return await UserService.delete_user(engine=session, token=user_data)
