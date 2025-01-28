# System
from typing import Annotated, Type
import logging

# Other libraries
from fastapi import APIRouter, status, Depends
from fastapi.responses import FileResponse

# Local
from src.api.core.category_app.schemas.category_dto import (
    CategoryIsUpdated,
    CategoryIsFinded,
    CategoriesList,
    CategoryBase,
    CategoryIsCreated,
    DataCategoryToUpdate,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.category_app.service.category_service import (
    CategoryService,
)
from src.api.dep.dependencies import EngineRepository, IEngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix

category_router = APIRouter(
    prefix=APIPrefix.CATEGORY_PREFIX.value,
    tags=[APITagsEnum.CATEGORY.value],
)

auth: Authentication = Authentication()
logger: Type[logging.Logger] = logging.getLogger(__name__)


@category_router.post(
    path="/create_new_category",
    description="""
    ### Endpoint - Создание новой категории товара.
    Данный метод позволяет создать новую категорию товара.
    Доступен для администратора.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Создание категории",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryIsCreated,
    tags=["AdminPanel - Панель администратора"],
)
async def create_new_category(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    new_category: CategoryBase,
) -> CategoryIsCreated:
    """
    ENDPOINT - Создание новой категории
    :param session:
    :param usr_data:
    :return:
    """

    logger.info(
        msg="Category-Router вызов метода создания"
        " новой категории (create_new_category)"
    )

    return await CategoryService.create_category(
        engine=session, token=admin_data, new_category=new_category
    )


@category_router.get(
    path="/get_icon_category/{id_category}",
    description="""
    ### Endpoint - Получение иконки категории.
    Метод для получения иконки категории по идентификатору.
    """,
    summary="Получение иконки категории",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
)
async def get_icon_category(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_category: int,
):
    return await CategoryService.get_icon_category(session, id_category)


@category_router.get(
    path="/find_category_by_name/{category_name}",
    description="""
    ### Endpoint - Поиск категории по названию.
    Необходимо передать в ссылке название категории
    """,
    summary="Поиск категории",
    response_model=CategoryIsFinded,
    status_code=status.HTTP_200_OK,
)
async def find_category_by_name(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    category_name: str,
) -> CategoryIsFinded:
    """
    ENDPOINT - Поиск категории
    :param session:
    :return:
    """

    logger.info(
        msg="Category-Router вызов метода получения"
        " категории по названию (find_category_by_name)"
    )

    return await CategoryService.find_category_by_name(
        engine=session,
        name_category=category_name,
        redis_search_data="category_by_name_%s" % category_name,
    )


@category_router.get(
    path="/get_all_category",
    description="""
    ### Endpoint - Получение всех категорий.
    Данный метод позволяет получить все имеющиеся категории.
    """,
    summary="Все категории",
    response_model=CategoriesList,
    status_code=status.HTTP_200_OK,
)
async def get_all_categories(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> CategoriesList:
    """
    ENDPOINT - Получение всех имеющихся категорий
    :param session:
    :return:
    """

    logger.info(
        msg="Category-Router вызов метода "
        "получения всех категорий (get_all_category)"
    )

    return await CategoryService.find_all_categories(
        engine=session, redis_search_data="all_categories"
    )


@category_router.get(
    path="/find_category_by_id/{id_category}",
    description="""
    ### Endpoint - Поиск категории по id.
    Данный метод осуществляет поиск категории по id.
    """,
    summary="Поиск категории по id",
    response_model=CategoryBase,
    status_code=status.HTTP_200_OK,
)
async def find_category_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_category: int,
) -> CategoryBase:
    """
    ENDPOINT - Поиск категории по id
    :param id_category:
    :return:
    """

    logger.info(
        msg="Category-Router вызов метода поиска"
        " категории по id (find_category_by_id)"
    )

    return await CategoryService.find_by_id(
        engine=session,
        id_category=id_category,
        redis_search_data="category_by_id_%s" % id_category,
    )


@category_router.patch(
    path="/update_category_name",
    description="""
    ### Endpoint - Обновление названия категории.
    Данный метод позволяет обновить название категории.
    Доступен только для администраторов.
    """,
    summary="Обновление названия категории",
    response_model=CategoryIsUpdated,
    status_code=status.HTTP_200_OK,
    tags=["AdminPanel"],
)
async def update_category_name(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    to_update: DataCategoryToUpdate,
) -> CategoryIsUpdated:
    """
    ENDPOINT - Обновление названия категории
    :param session:
    :param admin_data:
    :return:
    """

    logger.info(
        msg="Category-Router вызов метода обновления"
        " названия категории (update_category_name)"
    )

    return await CategoryService.update_category(
        engine=session, token=admin_data, data_to_update=to_update
    )


@category_router.delete(
    path="/delete_category/{id_category}",
    description="""
    ### Endpoint - Удаление категории.
    Данный метод позволяет удалять категории.
    Доступен для администраторов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Удаление категории",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["AdminPanel"],
)
async def delete_category(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_category: int,
) -> None:
    """
    ENDPOINT - удаление категории
    :param session:
    :param id_category:
    :return:
    """

    logger.info(
        msg="Category-Router вызов метода удаления категории (delete_category)"
    )

    await CategoryService.delete_category(
        engine=session, id_category=id_category, token=admin_data
    )
