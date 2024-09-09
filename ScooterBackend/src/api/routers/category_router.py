#System
from typing import Annotated

#Other libraries
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from src.api.dto.category_dto import *
from src.database.db_worker import db_work
from src.api.authentication.authentication_service import Authentication
from src.api.service.category_service import CategoryService
from src.api.dep.dependencies import EngineRepository, IEngineRepository

category_router = APIRouter(
    prefix="/category",
    tags=["Category - Категории товаров магазина"],
)

auth: Authentication = Authentication()


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
    tags=["AdminPanel - Панель администратора"]
)
async def create_new_category(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    new_category: CategoryBase
) -> CategoryIsCreated:
    """
    ENDPOINT - Создание новой категории
    :param session:
    :param usr_data:
    :return:
    """

    return await CategoryService.create_category(engine=session, token=admin_data, new_category=new_category)


@category_router.get(
    path="/find_category_by_name/{category_name}",
    description="""
    ### Endpoint - Поиск категории по названию.
    Необходимо передать в ссылке название категории
    """,
    summary="Поиск категории",
    response_model=CategoryIsFinded,
    status_code=status.HTTP_200_OK
)
async def find_category_by_name(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    category_name: str
) -> CategoryIsFinded:
    """
    ENDPOINT - Поиск категории
    :param session:
    :return:
    """

    return await CategoryService.find_category_by_name(engine=session, name_category=category_name)


@category_router.get(
    path="/get_all_category",
    description="""
    ### Endpoint - Получение всех категорий.
    Данный метод позволяет получить все имеющиеся категории.
    """,
    summary="Все категории",
    response_model=List[CategoryBase],
    status_code=status.HTTP_200_OK
)
async def get_all_categories(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> List[CategoryBase]:
    """
    ENDPOINT - Получение всех имеющихся категорий
    :param session:
    :return:
    """

    return await CategoryService.find_all_categories(engine=session)


@category_router.get(
    path="/find_category_by_id/{id_category}",
    description="""
    ### Endpoint - Поиск категории по id.
    Данный метод осуществляет поиск категории по id.
    """,
    summary="Поиск категории по id",
    response_model=CategoryBase,
    status_code=status.HTTP_200_OK
)
async def find_category_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_category: int
) -> CategoryBase:
    """
    ENDPOINT - Поиск категории по id
    :param id_category:
    :return:
    """

    return await CategoryService.find_by_id(engine=session, id_category=id_category)


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
    tags=["AdminPanel"]
)
async def update_category_name(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    to_update: DataCategoryToUpdate
) -> CategoryIsUpdated:
    """
    ENDPOINT - Обновление названия категории
    :param session:
    :param admin_data:
    :return:
    """

    return await CategoryService.update_category(engine=session, token=admin_data, data_to_update=to_update)


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
    tags=["AdminPanel"]
)
async def delete_category(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_category: int
) -> None:
    """
    ENDPOINT - удаление категории
    :param session:
    :param id_category:
    :return:
    """

    await CategoryService.delete_category(engine=session, id_category=id_category, token=admin_data)