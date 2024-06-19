#System
from typing import Annotated, List

#Other libraries
from fastapi import APIRouter, status, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.api.exception.http_product_exception import *
from ScooterBackend.api.dto.product_dto import *
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.database.db_worker import db_work
from ScooterBackend.api.service.product_service import ProductService


product_router: APIRouter = APIRouter(
    prefix="/product",
    tags=["Product - Товары магазина"]
)

auth: Authentication = Authentication()


@product_router.post(
    path="/create_product",
    description="""
    ### Endpoint - Создание продукта.
    Данный метод позволяет создать товар.
    Доступен только для администратора.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Создание товара",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductIsCreated,
    tags=["AdminPanel - Панель администратора"]
)
async def create_product(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    new_product: ProductBase
) -> ProductIsCreated:
    """
    ENDPOINT - Создание продукта
    :param session:
    :param admin_data:
    :param new_product:
    :return:
    """

    return await ProductService.create_product(session=session, token=admin_data, new_product=new_product)


@product_router.get(
    path="/get_all_products",
    description="""
    ### Endpoint - Получение всех товаров.
    Данный метод позволяет получить все имеющиеся товары.
    """,
    summary="Список товаров",
    status_code=status.HTTP_200_OK,
    response_model=Union[List, List[ProductBase]]
)
async def get_all_products(
    session: Annotated[AsyncSession, Depends(db_work.get_session)]
) -> Union[List, List[ProductBase]]:
    """
    ENDPOINT - Получение списка товаров.
    :param session:
    :return:
    """

    return await ProductService.get_all_products(session=session)


@product_router.get(
    path="/get_products_by_filter",
    description="""
    ### ENDPOINT - Получение продуктов по фильтрам поиска.
    Данный метод позволяет получить список продуктов по фильтрам поиска.
    """,
    summary="Поиск продуктов по фильтру",
    response_model=Union[List, List[ProductBase]],
    status_code=status.HTTP_200_OK
)
async def get_products_by_filters(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    id_category: int = None,
    min_price: int = None,
    max_price: int = None,
    desc_or_not: bool = False
) -> Union[List, List[ProductBase]]:
    """
    ENDPOINT - Получение списка продуктов по фильтру.
    :param id_category:
    :param min_price:
    :param max_price:
    """

    return await ProductService.get_products_by_sorted(
        session=session,
        sorted_by_category=id_category,
        sorted_by_price_min=min_price,
        sorted_by_price_max=max_price,
        desc=desc_or_not
    )


@product_router.get(
    path="/get_products_by_category",
    description="""
    ### Endpoint - Получение всех продуктов по определённой категории.
    Данный метод позволяет получить список всех продуктов по категории, можно передать как id категории так и название.
    """,
    summary="Получение всех товаров по категории",
    status_code=status.HTTP_200_OK,
    response_model=Union[List, List[ProductBase]]
)
async def get_products_by_category(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    category_data: Union[int, str]
) -> Union[List, List[ProductBase]]:
    """
    ENDPOINT - Получение списка товаров по категории
    :param session:
    :param category_data:
    :return:
    """

    return await ProductService.get_products_by_category(
        session=session,
        category_data=category_data
    )


@product_router.get(
    path="/find_product_by_id/{id_product}",
    description="""
    ### Endpoint - Поиск продукта по id.
    Позволяет информацию о продукте по id.
    Необходимо передать ид в ссылке запроса.
    """,
    summary="Поиск продукта по id",
    response_model=ProductBase,
    status_code=status.HTTP_200_OK
)
async def find_product_by_id(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    id_product: int
) -> ProductBase:
    """
    ENDPOINT - Поиск продукта по id
    :param session:
    :param id_product:
    :return:
    """

    return await ProductService.find_product_by_id(session=session, id_product=id_product)


@product_router.get(
    path="/get_product_by_name/{name_product}",
    description="""
    ### Endpoint - Получение продукта по названию.
    Данный метод позволяет получить информацию о продукте по названию.
    Необходимо передать название продукта в ссылку.
    """,
    summary="Получение продукта по названию",
    status_code=status.HTTP_200_OK,
    response_model=ProductBase
)
async def find_product_by_name(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    name_product: str
) -> ProductBase:
    """
    ENDPOINT - Поиск продукта по названию
    :param session:
    :param name_product:
    :return:
    """

    return await ProductService.find_product_by_name(session=session, name_product=name_product)


@product_router.get(
    path="/product_is_exists/{product_name}",
    description="""
    ### Endpoint- Проверка существования продукта.
    Необходимо передать в ссылку название продукта.
    """,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def product_is_created(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    product_name: str
) -> None:
    """
    ENDPOINT - Поиск продукта по названию
    :param session:
    :param product_name:
    :return:
    """

    return await ProductService.product_is_created(session=session, product_name=product_name)


@product_router.get(
    path="/get_all_information_about_product",
    description="""
    ### Endpoint - Получение всей информации о продукте.
    Данный метод позволяет получить всю информацию о продукте.
    """,
    summary="Вся информация о продукте",
    status_code=status.HTTP_200_OK,
    response_model=ProductAllInformation
)
async def get_all_information_about_product(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int
) -> ProductAllInformation:
    """
    ENDPOINT - Получение всей информации о товаре
    :param session:
    :param admin_data:
    :return:
    """

    return await ProductService.get_all_information_about_product(session=session, token=admin_data, id_product=id_product)


@product_router.get(
    path="/get_recommended_products",
    description="""
    ### Endpoint - Получение рекомендованных товаров.
    Данный метод позволяет получить товары по рекомендации
    """,
    summary="Рекомендованные товары",
    response_model=Union[List, List[ProductBase]],
    status_code=status.HTTP_200_OK
)
async def recommended_products(
    session: Annotated[AsyncSession, Depends(db_work.get_session)]
) -> Union[List, List[ProductBase]]:
    """
    Получение товаров по системе рекомендаций
    :session:
    """

    return await ProductService.get_recommended_products(session=session)


@product_router.put(
    path="/update_product_data",
    description="""
    ### Endpoint - Обновление информации о продукте.
    Данный метод позволяет обновить несколько или 1 поле о продукте.
    Доступен только для администратора.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Обновление информации о продукте",
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_information_about_product(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int,
    data_update: UpdateProduct
) -> None:
    """
    ENDPOINT - Обновление информации о продукте.
    :param session:
    :param id_product:
    :return:
    """

    return await ProductService.update_information(
        session=session,
        id_product=id_product,
        data_to_update=data_update,
        token=admin_data
    )


@product_router.patch(
    path="/update_product_photo/{product_id}",
    description="""
    ### Endpoint - Обновление фотографии продукта.
    Данный метод позволяет обновить фотографию продукта.
    Доступен только для администратора.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Обновление фотографии продукта",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def update_photo_product(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    product_id: int,
    new_photo: str,
) -> None:
    """
    ENDPOINT - Обновление фотографии товара
    :param session:
    :param admin_data:
    :param new_photo:
    :return:
    """

    return await ProductService.update_photo(
        session=session,
        photo_data=new_photo,
        token=admin_data,
        product_id=product_id
    )


@product_router.delete(
    path="/delete_product/{id_product}",
    description="""
    ### Endpoint - Удаление товара по id.
    Данный метод позволяет удалить товар, необходимо передать id продукта в ссылку! ПОЛЬЗОВАТЬСЯ АККУРАТНО.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке.
    """,
    summary="Удаление товара",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_product_by_id(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int
) -> None:
    """
    ENDPOINT - Удаление продукта по id.
    :param session:
    :param admin_data:
    :param id_product:
    :return:
    """

    return await ProductService.delete_product_by_id(session=session, id_product=id_product, token=admin_data)