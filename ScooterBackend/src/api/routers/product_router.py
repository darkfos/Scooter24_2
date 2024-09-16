#System
from typing import Annotated, List, Type

#Other libraries
from fastapi import APIRouter, status, Depends, UploadFile
from fastapi.responses import FileResponse

#Local
from src.api.exception.http_product_exception import *
from src.api.dto.product_dto import *
from src.api.authentication.authentication_service import Authentication
from src.database.db_worker import db_work
from src.api.service.product_service import ProductService
from src.api.dep.dependencies import IEngineRepository, EngineRepository


product_router: APIRouter = APIRouter(
    prefix="/product",
    tags=["Product - Товары магазина"]
)

auth: Type[Authentication] = Authentication()


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
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    photo_product: UploadFile,
    title_product: str,
    price_product: float,
    quantity_product: int,
    explanation_product: str,
    article_product: str,
    tags: str,
    other_data: str,
    price_discount: int,
    date_create_product: datetime.date = datetime.date.today(),
    date_update_information: datetime.date = datetime.date.today(),
) -> ProductIsCreated:
    """
    ENDPOINT - Создание продукта
    :param session:
    :param admin_data:
    :param new_product:
    :return:
    """

    return await ProductService.create_product(engine=session, token=admin_data, new_product=ProductBase(
        title_product=title_product,
        price_discount=price_discount,
        price_product=price_product,
        explanation_product=explanation_product,
        quantity_product=quantity_product,
        article_product=article_product,
        tags=tags,
        other_data=other_data,
        date_create_product=date_create_product,
        date_update_information=date_update_information,
        photo_product=""
    ), photo_product=photo_product)


@product_router.post(
    path="/add_new_category",
    description="""
    ### Endpoint - Добавление новой категории для товара.
    Данный метод позволяет добавить новую категорию для товара.
    """,
    summary="Добавление категории",
    status_code=status.HTTP_201_CREATED,
    response_model=None
)
async def add_new_category_to_product(
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_product: int,
    id_category: int
) -> None:
    
    return await ProductService.add_new_category(
        admin_data=user_data,
        engine=session,
        id_category=id_category,
        id_product=id_product
    )

@product_router.get(
    path="/get_all_products",
    description="""
    ### Endpoint - Получение всех товаров.
    Данный метод позволяет получить все имеющиеся товары.
    """,
    summary="Список товаров",
    status_code=status.HTTP_200_OK,
    response_model=ListProductBase
)
async def get_all_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListProductBase:
    """
    ENDPOINT - Получение списка товаров.
    :param session:
    :return:
    """

    return await ProductService.get_all_products(engine=session, redis_search_data="all_products")


@product_router.get(
    path="/get_products_by_filter",
    description="""
    ### ENDPOINT - Получение продуктов по фильтрам поиска.
    Данный метод позволяет получить список продуктов по фильтрам поиска.
    """,
    summary="Поиск продуктов по фильтру",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK
)
async def get_products_by_filters(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_category: int = None,
    min_price: int = None,
    max_price: int = None,
    desc_or_not: bool = False
) -> ListProductBase:
    """
    ENDPOINT - Получение списка продуктов по фильтру.
    :param id_category:
    :param min_price:
    :param max_price:
    """

    return await ProductService.get_products_by_sorted(
        engine=session,
        sorted_by_category=id_category,
        sorted_by_price_min=min_price,
        sorted_by_price_max=max_price,
        desc=desc_or_not,
        redis_search_data="search_by_filters_%s_%s_%s_%s" % (id_category, min_price, max_price, desc_or_not)
    )


@product_router.get(
    path="/get_products_by_category",
    description="""
    ### Endpoint - Получение всех продуктов по определённой категории.
    Данный метод позволяет получить список всех продуктов по категории, можно передать как id категории так и название.
    """,
    summary="Получение всех товаров по категории",
    status_code=status.HTTP_200_OK,
    response_model=ListProductBase
)
async def get_products_by_category_or_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    category_data: Union[int, str]
) -> ListProductBase:
    """
    ENDPOINT - Получение списка товаров по категории
    :param session:
    :param category_data:
    :return:
    """

    return await ProductService.get_products_by_category(
        engine=session,
        category_data=category_data,
        redis_search_data="find_products_by_id_category_%s" % category_data
    )


@product_router.get(
    path="/get_image_product/{photo_product_name}",
    description="""
    ### Endpoint - Получение картинки продукта по названию.
    Данный метод позволяет получить картинку продукта по названию
    """,
    summary="Получение изображения",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK
)
async def get_image_product(
    photo_product_name: str
) -> FileResponse:
    """
    ### Endpoint - Получение картинки продукта по названию.
    Данный метод позволяет получить картинку продукта по названию
    """
    
    return FileResponse(
        path=f"src/static/{photo_product_name}",
        filename="product_avatar.png",
        media_type="image/jpeg",
        status_code=status.HTTP_200_OK,
    )


@product_router.get(
    path="/product_is_exists/{product_name}",
    description="""
    ### Endpoint- Проверка существования продукта.
    Необходимо передать в ссылку название продукта.
    """,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def product_is_created(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    product_name: str
) -> None:
    """
    ENDPOINT - Поиск продукта по названию
    :param session:
    :param product_name:
    :return:
    """

    return await ProductService.product_is_created(engine=session, product_name=product_name)


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
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int
) -> ProductAllInformation:
    """
    ENDPOINT - Получение всей информации о товаре
    :param session:
    :param admin_data:
    :return:
    """

    return await ProductService.get_all_information_about_product(engine=session, token=admin_data, id_product=id_product, redis_search_data="full_information_about_product_by_id_%s" % id_product)


@product_router.get(
    path="/get_recommended_products",
    description="""
    ### Endpoint - Получение рекомендованных товаров.
    Данный метод позволяет получить товары по рекомендации
    """,
    summary="Рекомендованные товары",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK
)
async def recommended_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListProductBase:
    """
    ENDPOINT - Получение товаров по системе рекомендаций
    :session:
    """

    return await ProductService.get_recommended_products(engine=session, redis_search_data="recommended_products")


@product_router.get(
    path='/new_products',
    description="""
    ### Endpoint - Получение новых продуктов.
    Данный метод позволяет получить список из <8 новых продуктов
    """,
    summary="Новые продукты",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK
)
async def get_new_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListProductBase:
    """
    ENDPOINT - Получение новых товаров в количестве <8.
    :session:
    """

    return await ProductService.get_new_products(engine=session, redis_search_data="new_products")


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
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
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
        engine=session,
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
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
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
        engine=session,
        photo_data=new_photo,
        token=admin_data,
        product_id=product_id
    )


@product_router.patch(
    path="/update_product_discount",
    description="""
    ### Endpoint - Обновление скидки товара.
    Данный метод позволяет обновить скидку на товаре.
    Доступен только для администратораю
    Необходим jwt ключ и Bearer в заголовке запроса.""",
    summary="Обновление скидки",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_product_discount(
    session: Annotated[IEngineRepository, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int,
    data_to_update: UpdateProductDiscount
) -> None:
    """
    Обновление скидки товара
    :session:
    :admin_data:
    :data_to_update:
    """

    return await ProductService.update_product_discount(
        engine=session,
        token=admin_data,
        id_product=id_product,
        new_discount=data_to_update
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
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
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

    return await ProductService.delete_product_by_id(engine=session, id_product=id_product, token=admin_data)