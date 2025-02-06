# System
from typing import Annotated, Type, Union
import datetime
import logging

# Other libraries
from fastapi import APIRouter, Depends, UploadFile

# Local
from src.api.core.product_app.error.http_product_exception import status
from src.api.core.product_app.schemas.product_dto import (
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
from src.api.core.product_app.service.product_service import ProductService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from src.other.enums.product_enum import FilteredDescProduct


product_router: APIRouter = APIRouter(
    prefix=APIPrefix.PRODUCT_PREFIX.value, tags=[APITagsEnum.PRODUCT.value]
)

auth: Type[Authentication] = Authentication()
logger: Type[logging.Logger] = logging.getLogger(__name__)


@product_router.post(
    path="/create",
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
    admin_data: Annotated[str, Depends(auth.auth_user)],
    article_product: Annotated[str, Field(max_length=300)],
    title_product: Annotated[str, Field(max_length=500)],
    brand: int,
    brand_mark: int,
    id_s_sub_category: int,
    weight_product: Annotated[float, Field(ge=0)],
    explanation_product: Annotated[str, Field()],
    quantity_product: Annotated[int, Field(gt=-1)],
    price_product: Annotated[float, Field(gt=-1)],
    photo_product: Annotated[UploadFile, Field()],
    type_pr: int,
    product_discount: Annotated[int, Field(lt=100)],
    date_create_product: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ] = datetime.date.today(),
    date_update_information: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ] = datetime.date.today(),
    model: int = None,
    is_recommended: bool = False,
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
            id_product=None,
            label_product="1 год",
            is_recommended=is_recommended,
            type_pr=type_pr,
            article_product=article_product,
            title_product=title_product,
            brand=brand,
            brand_mark=brand_mark,
            models=model,
            id_sub_category=id_s_sub_category,
            weight_product=weight_product,
            explanation_product=explanation_product,
            quantity_product=quantity_product,
            price_product=price_product,
            photo=photo_product,
            date_create_product=date_create_product,
            date_update_information=date_update_information,
            product_discount=product_discount,  # noqa
        ),
        photo_product=photo_product,
    )


@product_router.post(
    path="/add/category",
    description="""
    ### Endpoint - Добавление новой категории для товара.
    Данный метод позволяет добавить новую категорию для товара.
    """,
    summary="Добавление категории",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def add_new_category_to_product(
    user_data: Annotated[str, Depends(auth.auth_user)],
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
    path="/all",
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
    path="/all/filter",
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
    title_product: Union[str, None] = None,
    id_category: int = None,
    id_sub_category: int = None,
    min_price: int = None,
    max_price: int = None,
    desc_or_not: FilteredDescProduct = FilteredDescProduct.DEFAULT,
    availability: bool = False,
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
        sorted_by_sub_category=id_sub_category,
        sorted_by_price_min=min_price,
        sorted_by_price_max=max_price,
        desc=desc_or_not,
        title_product=title_product,
        availability=availability,
        redis_search_data="search_by_filters_%s_%s_%s_%s"
        % (id_category, min_price, max_price, desc_or_not),
    )


@product_router.get(
    path="/all/category",
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
    path="/exists/{product_name}",
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
    path="/all/garage/filter",
    summary="Запчасти гаража",
    description="Товары подходящие под определенную технику из гаража",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK,
)
async def garage_products(
    user_data: Annotated[str, Depends(auth.auth_user)],
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    brand: Annotated[str, Field(max_length=100)] = None,
    model: Annotated[str, Field(max_length=100)] = None,
) -> ListProductBase:
    """
    Получение списка товаров под определенную модель и бренд

    :param user_data:
    :param session:
    :param brand:
    :param model:
    """

    return await ProductService.get_garage_products(
        token=user_data, engine=session, brand=brand, model=model
    )


@product_router.get(
    path="/information/full",
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
        id_product=id_product,
        redis_search_data="full_information_about_product_by_id_%s"
        % id_product,  # noqa
    )


@product_router.get(
    path="/last/sells",
    description="""
    ### ENDPOINT - Получение последних проданных товаров.
    Получаем список последних проданных товаров
    """,
    summary="Последние проданные товары",
    response_model=ListProductBase,
    status_code=status.HTTP_200_OK,
)
async def last_selled_products(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListProductBase:
    """
    Получение последних проданных товаров
    """

    return await ProductService.last_products(
        engine=session, redis_search_data="last_selled_products"
    )


@product_router.get(
    path="/recommends",
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
    path="/new",
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
    path="/update",
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
    admin_data: Annotated[str, Depends(auth.auth_user)],
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
    path="/update/discount",
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
    admin_data: Annotated[str, Depends(auth.auth_user)],
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
    path="/delete/{id_product}",
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
    admin_data: Annotated[str, Depends(auth.auth_user)],
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
