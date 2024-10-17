# System
from typing import Annotated, Type, Union
from datetime import datetime
import logging

# Other libraries
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse

# Local
from src.api.core.product_catalog.error.http_product_exception import status
from src.api.core.product_catalog.schemas.product_dto import (
    UpdateProduct,
    ProductBase,
    ProductAllInformation,
    ListProductBase,
    UpdateProductDiscount,
    ProductIsCreated,
    Field,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.database.db_worker import db_work
from src.api.core.product_catalog.service.product_service import ProductService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix


product_router: APIRouter = APIRouter(
    prefix=APIPrefix.PRODUCT_PREFIX.value, tags=[APITagsEnum.PRODUCT.value]
)

auth: Type[Authentication] = Authentication()
logger: Type[logging.Logger] = logging.getLogger(__name__)


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
    tags=["AdminPanel - Панель администратора"],
)
async def create_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    article_product: Annotated[str, Field(max_length=300)],
    title_product: Annotated[str, Field(max_length=500)],
    brand: int,
    brand_mark: int,
    model: int,
    id_s_sub_category: int,
    weight_product: Annotated[float, Field(ge=0)],
    explanation_product: Annotated[str, Field()],
    quantity_product: Annotated[int, Field(gt=-1)],
    price_product: Annotated[float, Field(gt=-1)],
    price_with_discount: Annotated[float, Field()],
    photo_product: Annotated[UploadFile, Field()],
    product_discount: Annotated[int, Field(lt=100)],
    date_create_product: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ] = datetime.date.today(),
    date_update_information: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ] = datetime.date.today(),
) -> ProductIsCreated:
    """
    ENDPOINT - Создание продукта
    :param session:
    :param admin_data:
    :param new_product:
    :return:
    """

    logger.info(
        msg="Product-Router вызов метода" " создания продукта (create_product)"
    )

    return await ProductService.create_product(
        engine=session,
        token=admin_data,
        new_product=ProductBase(
            article_product=article_product,
            title_product=title_product,
            brand=brand,
            brand_mark=brand_mark,
            model=model,
            id_s_sub_category=id_s_sub_category,
            weight_product=weight_product,
            explanation_product=explanation_product,
            quantity_product=quantity_product,
            price_product=price_product,
            price_with_discount=price_with_discount,
            photo_product=photo_product,
            date_create_product=date_create_product,
            date_update_information=date_update_information,
            product_discount=(price_product - price_with_discount)
            // price_product,  # noqa
        ),
        photo_product=photo_product,
    )


@product_router.post(
    path="/add_new_category",
    description="""
    ### Endpoint - Добавление новой категории для товара.
    Данный метод позволяет добавить новую категорию для товара.
    """,
    summary="Добавление категории",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def add_new_category_to_product(
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_product: int,
    id_category: int,
) -> None:

    logger.info(
        msg="Product-Router вызов метода добавления"
        " новой категории к товару (add_new_category)"
    )

    return await ProductService.add_new_category(
        admin_data=user_data,
        engine=session,
        id_category=id_category,
        id_product=id_product,
    )


@product_router.get(
    path="/get_all_products",
    description="""
    ### Endpoint - Получение всех товаров.
    Данный метод позволяет получить все имеющиеся товары.
    """,
    summary="Список товаров",
    status_code=status.HTTP_200_OK,
    response_model=ListProductBase,
)
async def get_all_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListProductBase:
    """
    ENDPOINT - Получение списка товаров.
    :param session:
    :return:
    """

    logger.info(
        msg="Product-Router вызов метода"
        " получения всех продуктов (get_all_products)"
    )

    return await ProductService.get_all_products(
        engine=session, redis_search_data="all_products"
    )


@product_router.get(
    path="/get_products_by_filter",
    description="""
    ### ENDPOINT - Получение продуктов по фильтрам поиска.
    Данный метод позволяет получить список продуктов по фильтрам поиска.
    """,
    summary="Поиск продуктов по фильтру",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK,
)
async def get_products_by_filters(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_category: int = None,
    min_price: int = None,
    max_price: int = None,
    desc_or_not: bool = False,
) -> ListProductBase:
    """
    ENDPOINT - Получение списка продуктов по фильтру.
    :param id_category:
    :param min_price:
    :param max_price:
    """

    logger.info(
        msg=f"Product-Router вызов метода получения продукта"
        f" по фильтрам id_category={id_category};"
        f" min_price={min_price};"
        f" max_price={max_price};"
        f" desc={desc_or_not} (get_products_by_filters)"
    )

    return await ProductService.get_products_by_sorted(
        engine=session,
        sorted_by_category=id_category,
        sorted_by_price_min=min_price,
        sorted_by_price_max=max_price,
        desc=desc_or_not,
        redis_search_data="search_by_filters_%s_%s_%s_%s"
        % (id_category, min_price, max_price, desc_or_not),
    )


@product_router.get(
    path="/get_products_by_category",
    description="""
    ### Endpoint - Получение всех продуктов по определённой категории.
    Данный метод позволяет получить список всех продуктов
    по категории, можно передать как id категории так и название.
    """,
    summary="Получение всех товаров по категории",
    status_code=status.HTTP_200_OK,
    response_model=ListProductBase,
)
async def get_products_by_category_or_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    category_data: Union[int, str],
) -> ListProductBase:
    """
    ENDPOINT - Получение списка товаров по категории
    :param session:
    :param category_data:
    :return:
    """

    logger.info(
        msg="Product-Router вызов метода получения"
        " продуктов по категории или "
        "по id (get_products_by_category_or_id)"
    )

    return await ProductService.get_products_by_category(
        engine=session,
        category_data=category_data,
        redis_search_data="find_products_by_id_category_%s" % category_data,
    )


@product_router.get(
    path="/get_image_product/{photo_product_name}",
    description="""
    ### Endpoint - Получение картинки продукта по названию.
    Данный метод позволяет получить картинку продукта по названию
    """,
    summary="Получение изображения",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_image_product(photo_product_name: str) -> FileResponse:
    """
    ### Endpoint - Получение картинки продукта по названию.
    Данный метод позволяет получить картинку продукта по названию
    """

    logger.info(
        msg="Product-Router вызов метода "
        "получения картинки товара (get_image_product)"
    )

    return FileResponse(
        path=f"src/static/images/{photo_product_name}",
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
    product_name: str,
) -> None:
    """
    ENDPOINT - Поиск продукта по названию
    :param session:
    :param product_name:
    :return:
    """

    logger.info(
        msg="Product-Router вызов метода проверка"
        " существования продукта (product_is_exists)"
    )

    return await ProductService.product_is_created(
        engine=session, product_name=product_name
    )


@product_router.get(
    path="/get_all_information_about_product",
    description="""
    ### Endpoint - Получение всей информации о продукте.
    Данный метод позволяет получить всю информацию о продукте.
    """,
    summary="Вся информация о продукте",
    status_code=status.HTTP_200_OK,
    response_model=ProductAllInformation,
)
async def get_all_information_about_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int,
) -> ProductAllInformation:
    """
    ENDPOINT - Получение всей информации о товаре
    :param session:
    :param admin_data:
    :return:
    """

    logger.info(
        msg="Product-Router вызов метода получения полной "
        "информации о продукте (get_all_information_about_product)"
    )

    return await ProductService.get_all_information_about_product(
        engine=session,
        token=admin_data,
        id_product=id_product,
        redis_search_data="full_information_about_product_by_id_%s"
        % id_product,  # noqa
    )


@product_router.get(
    path="/get_recommended_products",
    description="""
    ### Endpoint - Получение рекомендованных товаров.
    Данный метод позволяет получить товары по рекомендации
    """,
    summary="Рекомендованные товары",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK,
)
async def recommended_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListProductBase:
    """
    ENDPOINT - Получение товаров по системе рекомендаций
    :session:
    """

    logger.info(
        msg="Product-Router вызов метода получения "
        "рекомендованных товаров (get_recommended_products)"
    )

    return await ProductService.get_recommended_products(
        engine=session, redis_search_data="recommended_products"
    )


@product_router.get(
    path="/new_products",
    description="""
    ### Endpoint - Получение новых продуктов.
    Данный метод позволяет получить список из <8 новых продуктов
    """,
    summary="Новые продукты",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK,
)
async def get_new_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListProductBase:
    """
    ENDPOINT - Получение новых товаров в количестве <8.
    :session:
    """

    logger.info(
        msg="Product-Router вызов метода получения "
        "новых продуктов (new_products)"
    )

    return await ProductService.get_new_products(
        engine=session, redis_search_data="new_products"
    )


@product_router.put(
    path="/update_product_data",
    description="""
    ### Endpoint - Обновление информации о продукте.
    Данный метод позволяет обновить несколько или 1 поле о продукте.
    Доступен только для администратора.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Обновление информации о продукте",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_information_about_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int,
    data_update: UpdateProduct,
) -> None:
    """
    ENDPOINT - Обновление информации о продукте.
    :param session:
    :param id_product:
    :return:
    """

    logger.info(
        msg="Product-Router вызов метода"
        " обновления информации о продукте (update_product_data)"
    )

    return await ProductService.update_information(
        engine=session,
        id_product=id_product,
        data_to_update=data_update,
        token=admin_data,
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
    response_model=None,
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

    logger.info(
        msg="Product-Router вызов метода"
        " обновления фотографии продукта (update_photo_product)"
    )

    return await ProductService.update_photo(
        engine=session,
        photo_data=new_photo,
        token=admin_data,
        product_id=product_id,
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
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_product_discount(
    session: Annotated[IEngineRepository, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int,
    data_to_update: UpdateProductDiscount,
) -> None:
    """
    Обновление скидки товара
    :session:
    :admin_data:
    :data_to_update:
    """

    logger.info(
        msg="Product-Router вызов метода "
        "обновления скидки товара (update_product_discount)"
    )

    return await ProductService.update_product_discount(
        engine=session,
        token=admin_data,
        id_product=id_product,
        new_discount=data_to_update,
    )


@product_router.delete(
    path="/delete_product/{id_product}",
    description="""
    ### Endpoint - Удаление товара по id.
    Данный метод позволяет удалить товар, необходимо передать
    id продукта в ссылку! ПОЛЬЗОВАТЬСЯ АККУРАТНО.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке.
    """,
    summary="Удаление товара",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_product_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_product: int,
) -> None:
    """
    ENDPOINT - Удаление продукта по id.
    :param session:
    :param admin_data:
    :param id_product:
    :return:
    """

    logger.info(
        msg="Product-Router вызов метода удаления"
        " продукта по id (delete_product_by_id)"
    )

    return await ProductService.delete_product_by_id(
        engine=session, id_product=id_product, token=admin_data
    )
