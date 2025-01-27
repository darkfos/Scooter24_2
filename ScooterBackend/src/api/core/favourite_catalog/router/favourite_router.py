# System
from typing import Annotated, Type, Union, List
import logging


# Other libraries
from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


# Local
from src.api.core.favourite_catalog.schemas.favourite_dto import (
    FavouriteInformation,
    FavouriteSmallData,
    AddFavourite,
    ListFavouriteBase,
)

from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.favourite_catalog.service.favourite_service import (
    FavouriteService,
)
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix


auth: Authentication = Authentication()
favourite_router: APIRouter = APIRouter(
    prefix=APIPrefix.FAVOURITE_PREFIX.value, tags=[APITagsEnum.FAVOURITE.value]
)
logger: Type[logging.Logger] = logging.getLogger(__name__)


@favourite_router.post(
    path="/create_a_new_favourite_product",
    description="""
    ### Endpoint - Добавление нового товара в список избранных.
    Данный метод позволяет добавить продукт в список избранных.
    Необходим jwt токен и Bearer в заголовке запроса.
    """,
    summary="Добавление избранного товара",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def create_a_new_favourite(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    new_favourite: AddFavourite,
) -> dict:
    """
    ENDPOINT - Добавление нового товара в избранное
    :param session:
    :param user_data:
    :param new_favourite:
    :return:
    """

    logger.info(
        msg="Favourite-Router вызов метода создания"
        " нового товара в списке избранных (create_a_new_favourite_product)"
    )

    return {"id_fav" : await FavouriteService.create_favourite_product(
        engine=session, token=user_data, new_product_in_favourite=new_favourite
    )}


@favourite_router.get(
    path="/get_all_favourites_by_user_id",
    description="""
    ### Endpoint - Все избранные товары пользователя.
    Данный метод предоставляет информацию обо всех
    избранных товарах пользователя.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Список избранных товаров",
    status_code=status.HTTP_200_OK,
    response_model=ListFavouriteBase,
)
async def get_all_favourites_products_by_user_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
) -> ListFavouriteBase:
    """
    ENDPOINT - Получение всех избранных товаров пользователя
    :param session:
    :param user_data:
    :param id_user:
    :return:
    """

    logger.info(
        msg="Favourite-Router вызов метода получения списка"
        " всех избранных товаров по"
        " идентификатору пользователя (get_all_favourites_by_user_id)"
    )

    return await FavouriteService.get_all_favourite_product_by_user_id(
        engine=session,
        token=user_data,
        redis_search_data="all_favourites_by_id_user_%s" % user_data,
    )


@favourite_router.get(
    path="/get_favourite_data_for_id/{id_fav_product}",
    description="""
    ### Endpoint - Получение информации о избранном товаре по id.
    Данный метод позволяет получить полную информацию об избранном товаре.
    Доступно для администраторов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Детальная информация об избранном товаре",
    status_code=status.HTTP_200_OK,
    response_model=FavouriteInformation,
    tags=["AdminPanel - Панель администратора"],
)
async def get_full_information_about_favourite_product_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[AsyncSession, Depends(auth.auth_user)],
    id_fav_product: int,
) -> FavouriteInformation:
    """
    ENDPOINT - Получение полной информации о продукте по его id
    :param session:
    :param id_fav_product:
    :return:
    """

    logger.info(
        msg="Favourite-Router вызов метода получения полной"
        " информации о избранном товаре по "
        "id (get_full_information_about_favourite_product_by_id)"
    )

    return await FavouriteService.get_information_about_fav_product_by_id(
        engine=session,
        token=admin_data,
        id_fav_product=id_fav_product,
    )


@favourite_router.get(
    path="/get_all_favourites",
    description="""
    ### Endpoint - Получение всех избранных товаров.
    Данный метод позволяет получить все избранные товары.
    Доступен для администратора.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Все избранные товары",
    status_code=status.HTTP_200_OK,
    response_model=Union[List, List[FavouriteSmallData]],
    tags=["AdminPanel - Панель администратора"],
)
async def get_all_favourites_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
) -> Union[List, List[FavouriteSmallData]]:
    """
    ENDPOINT - Получение информации обо всех избранных товаров
    :param session:
    :param admin_data:
    :return:
    """

    logger.info(
        msg="Favourite-Router вызов метода получения"
        " всех избранных товаров (get_all_favourites_products)"
    )

    return await FavouriteService.get_all_favourites(
        engine=session, token=admin_data
    )


@favourite_router.delete(
    path="/delete_favourite_product",
    description="""
    ### Endpoint - Удаление избранного товара пользователя.
    Данный метод позволяет удалить товар из избранного списка.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Удаление избранного товара",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_favourite_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    id_favourite: int,
) -> None:
    """
    ENDPOINT - Удаление товара из списка избранных
    :param session:
    :param user_data:
    :param id_favourite:
    :return:
    """

    logger.info(
        msg="Favourite-Router вызов метода удаления товара"
        " из списка избранных по id (delete_favourite_product)"
    )

    return await FavouriteService.delete_favourite_product(
        engine=session, token=user_data, id_favourite=id_favourite
    )
