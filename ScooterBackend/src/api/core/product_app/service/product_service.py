# System
import datetime
import logging as logger
from typing import Union, List, Type
from fastapi import status, HTTPException, UploadFile

from src.api.core.subcategory_app.schemas.subcategory_dto import (
    SubCategoryAllData,
)

# Local
from src.database.models.product import Product
from src.api.core.product_app.error.http_product_exception import (
    ProductHttpError,
)
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.api.core.category_app.error.http_category_exception import (
    CategoryHttpError,
)
from src.api.core.product_app.schemas.product_dto import (
    ListProductBase,
    ProductBase,
    ProductAllInformation,
    ProductIsCreated,
    UpdateProduct,
    UpdateProductDiscount,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.product_enum import FilteredDescProduct
from src.other.image.image_saver import ImageSaver
from src.other.enums.auth_enum import AuthenticationEnum
from src.other.s3_service.file_manager import FileS3Manager
from src.database.models.product_photos import ProductPhotos
from src.api.core.type_moto_app.schemas.type_moto_dto import ProductTypeModels
from src.api.core.mark_app.schemas.mark_dto import ProductMarks


# Redis
from src.store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class ProductService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_product(
        engine: IEngineRepository,
        token: str,
        new_product: ProductBase,
        photo_product: UploadFile,
        token_data: dict = dict(),
    ) -> ProductIsCreated:
        """
        Метод для создания нового продукта
        :param session:
        :param token:
        :param new_product:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} " f"Создание нового продукта"
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = await engine.user_repository.find_admin(
                id_=int(token_data.get("sub"))
            )

            if is_admin:

                # Сохраняем фотографию в хранилище
                file_manager = FileS3Manager()
                url_file = await file_manager.upload_file_to_storage(
                    file=photo_product
                )

                if not url_file:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Не удалось загрузить фотографию продукта",
                    )

                product = Product(
                    label_product=new_product.label_product,
                    title_product=new_product.title_product,
                    price_product=new_product.price_product,
                    article_product=new_product.article_product,
                    brand=new_product.brand,
                    brand_mark=new_product.brand_mark,
                    # model=new_product.model,
                    date_create_product=new_product.date_create_product,
                    date_update_information=new_product.date_update_information,
                    id_sub_category=new_product.id_sub_category,
                    product_discount=new_product.product_discount,
                    quantity_product=new_product.quantity_product,
                )
                # Create product
                product_is_created: bool = (
                    await engine.product_repository.add_one(data=product)
                )

                if product_is_created:
                    saved_photo_product = (
                        await engine.photos_repository.add_one(
                            ProductPhotos(
                                id_product=product_is_created,
                                photo_url=url_file,
                            )
                        )
                    )

                    if saved_photo_product:

                        if saved_photo_product and product_is_created:
                            return ProductIsCreated(
                                is_created=True,
                                product_name=product_is_created,
                            )

                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Не удалось загрузить фотографию продукта",
                    )
            logging.critical(
                msg=f"{ProductService.__name__} "
                f"Не удалось создать новый продукт"
            )
            await ProductHttpError().http_failed_to_create_a_new_product()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def add_new_category(
        engine: IEngineRepository,
        id_product: int,
        id_category: int,
        admin_data: str,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для добавления новой категории для товара
        :param engine:
        :param id_product:
        :param id_category:
        :param admin_data:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Добавление новой категории для товара"
        )

        async with engine:
            is_admin = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=token_data.get("email"),
                )
            )
            if is_admin:
                created_new_category_for_product = (
                    await engine.product_category_repository.add_new_category(
                        id_category=id_category, id_product=id_product
                    )
                )
                return (
                    True
                    if created_new_category_for_product
                    else (
                        await CategoryHttpError().http_failed_to_create_a_new_category()  # noqa
                    )
                )
            logging.critical(
                msg=f"{ProductService.__name__} "
                f"Не удалось добавить новую "
                f"категорию к товару"
            )
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_all_products(
        engine: IEngineRepository, redis_search_data: str
    ) -> ListProductBase:
        """
        Метод сервиса для получения всех товаров
        :param session:
        :return:
        """

        logging.info(msg=f"{ProductService.__name__} Получение всех товаров")
        async with engine:
            all_products = await engine.product_repository.find_all()

            if all_products:
                return ListProductBase(
                    products=[
                        ProductBase(
                            id_product=product[0].id,
                            label_product=product[0].label_product,
                            article_product=product[0].article_product,
                            title_product=product[0].title_product,
                            brand=product[0].brand,
                            brand_mark=[],
                            models=[],
                            id_sub_category=product[0].id_sub_category,
                            weight_product=product[0].weight_product,
                            is_recommended=product[0].is_recommended,
                            explanation_product=product[0].explanation_product,
                            quantity_product=product[0].quantity_product,
                            price_product=product[0].price_product,
                            date_create_product=product[0].date_create_product,
                            date_update_information=product[
                                0
                            ].date_update_information,
                            product_discount=product[0].product_discount,
                            type_pr=[],
                            photo=[],
                        )
                        for product in all_products
                    ]
                )

            return ListProductBase(products=[])

    @redis
    @staticmethod
    async def last_products(
        engine: IEngineRepository,
        redis_search_data: str,
    ) -> ListProductBase:
        """
        Получение последних проданных товаров
        """

        logging.info(
            msg=f"{ProductService.__name__} получение последних проданных товаров"  # noqa
        )  # noqa

        async with engine:
            products = await engine.order_repository.get_last_products()
            product_data = ListProductBase(products=[])
            for product in products:
                product_data.products.append(
                    ProductBase(
                        id_product=product[0].product_info.id,
                        label_product=product[0].product_info.label_product,
                        article_product=product[
                            0
                        ].product_info.article_product,
                        title_product=product[0].product_info.title_product,
                        brand=product[0].product_info.brand,
                        brand_mark=[
                            ProductMarks(
                                id_product=mark.id_product,
                                id_mark=mark.id_mark,
                            )
                            for mark in product[0].product_info.brand_mark
                        ],
                        models=[
                            model.read_model()
                            for model in product[
                                0
                            ].product_info.product_models_data
                        ],
                        id_sub_category=product[
                            0
                        ].product_info.id_sub_category,
                        weight_product=product[0].product_info.weight_product,
                        is_recommended=product[0].product_info.is_recommended,
                        explanation_product=product[
                            0
                        ].product_info.explanation_product,
                        quantity_product=product[
                            0
                        ].product_info.quantity_product,
                        price_product=product[0].product_info.price_product,
                        date_create_product=product[
                            0
                        ].product_info.date_create_product,
                        date_update_information=product[
                            0
                        ].product_info.date_update_information,
                        product_discount=product[
                            0
                        ].product_info.product_discount,
                        photo=[
                            photo.read_model()
                            for photo in product[0].product_info.photos
                        ],
                        type_pr=[
                            ProductTypeModels(
                                id_product=type_pr.id_product,
                                id_moto_type=type_pr.id_type_model,
                            )
                            for type_pr in product[0].product_info.type_models
                        ],
                    )
                )

            return product_data

    @staticmethod
    async def get_garage_products(
        token: str,
        engine: IEngineRepository,
        id_brand: int = None,
        id_model: int = None,
        id_moto_type: int = None,
    ) -> ListProductBase:
        """
        Получение всех товаров для гаража по модели и бренду
        """

        async with engine:
            req = await engine.product_repository.find_to_garage(
                id_brand=id_brand, id_model=id_model, id_moto_type=id_moto_type
            )

            return ListProductBase(
                products=[
                    ProductBase(
                        id_product=product[0].id,
                        label_product=product[0].label_product,
                        article_product=product[0].article_product,
                        title_product=product[0].title_product,
                        brand=product[0].brand,
                        brand_mark=[
                            ProductMarks(
                                id_product=mark.id_product,
                                id_mark=mark.id_mark,
                            )
                            for mark in product[0].brand_mark
                        ],
                        models=[],
                        id_sub_category=product[0].id_sub_category,
                        weight_product=product[0].weight_product,
                        is_recommended=product[0].is_recommended,
                        explanation_product=product[0].explanation_product,
                        quantity_product=product[0].quantity_product,
                        price_product=product[0].price_product,
                        date_create_product=product[0].date_create_product,
                        date_update_information=product[
                            0
                        ].date_update_information,
                        product_discount=product[0].product_discount,
                        photo=[
                            photo.read_model() for photo in product[0].photos
                        ],
                        type_pr=[
                            ProductTypeModels(
                                id_product=product.id_product,
                                id_moto_type=product.id_type_model,
                            )
                            for product in product[0].type_models
                        ],
                    )
                    for product in req
                ]
            )

    @staticmethod
    async def search_products(
        engine: IEngineRepository, id_mark: str = None, id_model: str = None
    ) -> ListProductBase:

        async with engine:
            products = await engine.product_repository.search(
                id_mark=id_mark, id_model=id_model
            )

            return ListProductBase(
                products=[
                    ProductBase(
                        id_product=product[0].id,
                        label_product=product[0].label_product,
                        article_product=product[0].article_product,
                        title_product=product[0].title_product,
                        brand=product[0].brand,
                        brand_mark=[
                            ProductMarks(
                                id_product=mark.id_product,
                                id_mark=mark.id_mark,
                            )
                            for mark in product[0].brand_mark
                        ],
                        models=[],
                        id_sub_category=product[0].id_sub_category,
                        weight_product=product[0].weight_product,
                        is_recommended=product[0].is_recommended,
                        explanation_product=product[0].explanation_product,
                        quantity_product=product[0].quantity_product,
                        price_product=product[0].price_product,
                        date_create_product=product[0].date_create_product,
                        date_update_information=product[
                            0
                        ].date_update_information,
                        product_discount=product[0].product_discount,
                        photo=[
                            photo.read_model() for photo in product[0].photos
                        ],
                        type_pr=[
                            ProductTypeModels(
                                id_product=product.id_product,
                                id_moto_type=product.id_type_model,
                            )
                            for product in product[0].type_models
                        ],
                    )
                    for product in products
                ]
            )

    @redis
    @staticmethod
    async def get_products_by_category(
        engine: IEngineRepository,
        category_data: Union[str, int],
        redis_search_data: str,
    ) -> Union[List, List[ProductBase]]:
        """
        Метод сервиса для получения списка товаров по категории
        :param session:
        :param category_data:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Получение списка товаров по категории "
            f"category_data={category_data}"
        )
        async with engine:
            all_products: Union[List, List[Product]] = (
                await engine.product_repository.find_by_category(
                    how_to_find=(
                        category_data
                        if not category_data.isdigit()
                        else int(category_data)
                    )
                )
            )

            if all_products:
                return ListProductBase(
                    products=[
                        ProductBase(
                            id_product=product[0].id,
                            label_product=product[0].label_product,
                            article_product=product[0].article_product,
                            title_product=product[0].title_product,
                            brand=product[0].brand,
                            brand_mark=[
                                ProductMarks(
                                    id_product=mark.id_product,
                                    id_mark=mark.id_mark,
                                )
                                for mark in product[0].brand_mark
                            ],
                            models=[],
                            id_sub_category=product[0].id_sub_category,
                            weight_product=product[0].weight_product,
                            is_recommended=product[0].is_recommended,
                            explanation_product=product[0].explanation_product,
                            quantity_product=product[0].quantity_product,
                            price_product=product[0].price_product,
                            date_create_product=product[0].date_create_product,
                            date_update_information=product[
                                0
                            ].date_update_information,
                            product_discount=product[0].product_discount,
                            photo=[
                                photo.read_model()
                                for photo in product[0].photos
                            ],
                            type_pr=[
                                ProductTypeModels(
                                    id_product=product.id_product,
                                    id_moto_type=product.id_type_model,
                                )
                                for product in product[0].type_models
                            ],
                        )
                        for product in all_products
                    ]
                )

            return ListProductBase(products=[])

    @staticmethod
    async def find_product_by_id(
        engine: IEngineRepository, id_product: int
    ) -> ProductBase:
        """
        Метод сервиса для поиска продукта по id
        :param session:
        :param id_product:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Поиск продукта по id={id_product}"
        )
        async with engine:
            product_data = await engine.product_repository.find_one(
                other_id=id_product
            )

            if product_data:
                return ProductBase(
                    id_product=product_data[0].id,
                    label_product=product_data[0].label_product,
                    article_product=product_data[0].article_product,
                    title_product=product_data[0].title_product,
                    brand=product_data[0].brand,
                    brand_mark=[],
                    models=[],
                    id_sub_category=product_data[0].id_sub_category,
                    weight_product=product_data[0].weight_product,
                    is_recommended=product_data[0].is_recommended,
                    explanation_product=product_data[0].explanation_product,
                    quantity_product=product_data[0].quantity_product,
                    price_product=product_data[0].price_product,
                    date_create_product=product_data[0].date_create_product,
                    date_update_information=product_data[
                        0
                    ].date_update_information,
                    product_discount=product_data[0].product_discount,
                    photo=[],
                    type_pr=[],
                )

            logging.critical(
                msg=f"{ProductService.__name__} "
                f"Не удалось удалить продукт по "
                f"id={id_product}"
            )
            await ProductHttpError().http_product_not_found()

    @staticmethod
    async def find_product_by_name(
        engine: IEngineRepository, name_product: str
    ) -> ProductBase:
        """
        Метод сервиса для поиска продукта по названию
        :param session:
        :param name_product:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Поиск продукта по name={name_product}"
        )
        async with engine:
            product_data: Union[None, Product] = (
                await engine.product_repository.find_product_by_name(
                    name_product=name_product
                )
            )

            if product_data:
                return ProductBase(
                    id_product=product_data[0].id,
                    label_product=product_data[0].label_product,
                    article_product=product_data[0].article_product,
                    title_product=product_data[0].title_product,
                    brand=product_data[0].brand,
                    brand_mark=product_data[0].brand_mark,
                    models=[],
                    id_sub_category=product_data[0].id_sub_category,
                    weight_product=product_data[0].weight_product,
                    is_recommended=product_data[0].is_recommended,
                    explanation_product=product_data[0].explanation_product,
                    quantity_product=product_data[0].quantity_product,
                    price_product=product_data[0].price_product,
                    date_create_product=product_data[0].date_create_product,
                    date_update_information=product_data[
                        0
                    ].date_update_information,
                    product_discount=product_data[0].product_discount,
                    photo=[],
                    type_pr=product_data[0].type_pr,
                )

            logging.critical(
                msg=f"{ProductService.__name__} " f"Не удалось найти продукт"
            )
            await ProductHttpError().http_product_not_found()

    @staticmethod
    async def product_is_created(
        engine: IEngineRepository, product_name: str
    ) -> None:
        """
        Метод сервиса для проверки что продукт существует
        :param session:
        :param product_name:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Проверка существования продукта"
        )

        async with engine:
            product_is_created = (
                await engine.product_repository.find_product_by_name(
                    name_product=product_name
                )
            )

            if product_is_created:
                return True
            logging.critical(
                msg=f"{ProductService.__name__} " f"Не удалось найти продукт"
            )
            await ProductHttpError().http_product_not_found()

    @redis
    @staticmethod
    async def get_all_information_about_product(
        engine: IEngineRepository,
        id_product: int,
        redis_search_data: str,
    ) -> ProductAllInformation:
        """
        Метод сервиса для получения полной информации о продукте
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Получение полной информации о продукте"
        )

        async with engine:
            product_data: Union[None, Product] = (
                await engine.product_repository.get_all_info(
                    id_product=id_product
                )
            )

            if product_data:
                return ProductAllInformation(
                    id_product=product_data[0].id,
                    label_product=product_data[0].label_product,
                    article_product=product_data[0].article_product,
                    title_product=product_data[0].title_product,
                    brand=product_data[0].brand,
                    brand_mark=[
                        ProductMarks(
                            id_product=mark.id_product, id_mark=mark.id_mark
                        )
                        for mark in product_data[0].brand_mark
                    ],
                    models=[
                        model.read_model()
                        for model in product_data[0].product_models_data
                    ],
                    id_sub_category=product_data[0].id_sub_category,
                    weight_product=product_data[0].weight_product,
                    is_recommended=product_data[0].is_recommended,
                    explanation_product=product_data[0].explanation_product,
                    quantity_product=product_data[0].quantity_product,
                    price_product=product_data[0].price_product,
                    date_create_product=product_data[0].date_create_product,
                    date_update_information=product_data[
                        0
                    ].date_update_information,
                    product_discount=product_data[0].product_discount,
                    photo=[
                        photo.read_model() for photo in product_data[0].photos
                    ],
                    type_pr=[
                        ProductTypeModels(
                            id_product=tp.id_product,
                            id_moto_type=tp.id_type_model,
                        )
                        for tp in product_data[0].type_models
                    ],
                    reviews=[
                        review_p.read_model()
                        for review_p in product_data[0].reviews
                    ],
                    orders=[
                        order_pr.read_model()
                        for order_pr in product_data[0].orders_list
                    ],  # noqa
                    favourites=[
                        fav_p.read_model()
                        for fav_p in product_data[0].product_info_for_fav
                    ],
                    categories=SubCategoryAllData(
                        name=product_data[0].sub_category_data.name,
                        id_subcategory=product_data[0].sub_category_data.id,
                        id_category=product_data[
                            0
                        ].sub_category_data.id_category,
                    ),
                )
            logging.critical(
                msg=f"{ProductService.__name__} " f"Не удалось найти продукт"
            )
            await ProductHttpError().http_product_not_found()
        logging.critical(
            msg=f"{ProductService.__name__} "
            f"Не удалось найти продукт, "
            f"пользователь не был найден"
        )
        await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_information(
        engine: IEngineRepository,
        id_product: int,
        token: str,
        data_to_update: UpdateProduct,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для обновления информации о продукте
        :param session:
        :param id_product:
        :param token:
        :param data_to_update:
        :return:
        """

        async with engine:
            # Is admin
            is_admin: bool = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin and is_admin.id_type_user == 2:
                # Update data
                is_updated: bool = await engine.product_repository.update_one(
                    other_id=id_product,
                    data_to_update=data_to_update.model_dump(),
                )

                if is_updated:
                    return
                logging.critical(
                    msg=f"{ProductService.__name__} "
                    f"Не удалось обновить продукт,"
                    f" продукт не был найден"
                )
                (
                    await ProductHttpError().http_failed_to_update_product_information()  # noqa
                )
            logging.critical(
                msg=f"{ProductService.__name__} "
                f"Не удалось обновить продукт,"
                f" пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_photo(
        engine: IEngineRepository,
        token: str,
        photo_data: str,
        product_id: int,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для обновления фотографии товара
        :param session:
        :param token:
        :param photo_data:
        :return:
        """

        logging.info(msg=f"{ProductService.__name__} Обновление фотографии")

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                # Обновление фотографии
                await engine.product_repository.update_one(
                    other_id=product_id,
                    data_to_update={
                        "photo_product": str(product_id) + "_" + photo_data,
                        "date_update_information": datetime.date.today(),
                    },
                )
                return
            logging.critical(
                msg=f"{ProductService.__name__} "
                f"Не удалось обновить фотографию"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_product_by_id(
        engine: IEngineRepository,
        token: str,
        id_product: int,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для удаления продукта по id
        :param session:
        :param token:
        :param id_product:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Удаление продукта по id = {id_product}"
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                product_data: Product = (
                    await engine.product_repository.find_one(
                        other_id=id_product
                    )
                )
                if product_data:
                    product_data = product_data[0]

                is_del: bool = await engine.product_repository.delete_one(
                    other_id=id_product
                )
                if is_del:
                    # Delete photo
                    image = ImageSaver()
                    image.filename = product_data.photo_product
                    await image.remove_file()
                    return
                logging.critical(
                    msg=f"{ProductService.__name__} "
                    f"Не удалось удалить продукт по "
                    f"id = {id_product}"
                )
                await ProductHttpError().http_failed_to_delete_product()
            logging.info(
                msg=f"{ProductService.__name__} "
                f"Не удалось удалить продукт по "
                f"id = {id_product}, "
                f"пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_products_by_sorted(
        engine: IEngineRepository,
        desc: FilteredDescProduct,
        redis_search_data: str,
        sorted_by_category: int = None,
        sorted_by_sub_category: int = None,
        sorted_by_price_min: int = None,
        sorted_by_price_max: int = None,
        title_product: str = None,
        availability: bool = False,
    ) -> ListProductBase:
        """
        Метод сервиса для поиска товаров, а также их сортировки
        :param session:
        :param token:
        :param id_product:
        :return:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Поиск продуктов по требованиям "
            f"desc={desc}, "
            f"category={sorted_by_category}, "
            f"min_price={sorted_by_price_min}, "
            f"max_price={sorted_by_price_max}"
        )

        async with engine:
            # Получаем товары
            products: Union[List, List[ProductBase]] = (
                await engine.product_repository.find_by_filters(
                    id_categories=sorted_by_category,
                    id_sub_category=sorted_by_sub_category,
                    min_price=sorted_by_price_min,
                    max_price=sorted_by_price_max,
                    title_product=title_product,
                    desc=desc,
                    availability=availability,
                )
            )

            if products:
                return ListProductBase(
                    products=[
                        ProductBase(
                            id_product=product.id,
                            label_product=product.label_product,
                            type_pr=[
                                ProductTypeModels(
                                    id_moto_type=tp.id_type_model,
                                    id_product=tp.id_product,
                                )
                                for tp in product.type_models
                            ],
                            article_product=product.article_product,
                            title_product=product.title_product,
                            brand=product.brand,
                            brand_mark=[
                                ProductMarks(
                                    id_mark=mark.id_mark,
                                    id_product=mark.id_product,
                                )
                                for mark in product.brand_mark
                            ],
                            models=[
                                model.read_model()
                                for model in product.product_models_data
                            ],
                            id_sub_category=product.id_sub_category,
                            weight_product=product.weight_product,
                            is_recommended=product.is_recommended,
                            explanation_product=product.explanation_product,
                            quantity_product=product.quantity_product,
                            price_product=product.price_product,
                            date_create_product=product.date_create_product,
                            date_update_information=product.date_update_information,  # noqa
                            product_discount=product.product_discount,
                            photo=(
                                [
                                    photo.read_model()
                                    for photo in product.photos
                                ]
                                if product.photos
                                else []
                            ),
                        ).model_dump()
                        for product in products
                    ]
                )
            return ListProductBase(products=[])

    @redis
    @staticmethod
    async def get_recommended_products(
        engine: IEngineRepository, redis_search_data: str
    ) -> Union[List, ListProductBase]:
        """
        Метод сервиса для получения рекомендованных товаров.
        :session:
        """

        logging.info(
            msg=f"{ProductService.__name__} "
            f"Получение рекомендованных товаров"
        )

        async with engine:
            # Получение всех товаров
            products_data: List[Product] = (
                await engine.product_repository.get_recommended_products()
            )
            data_result: ListProductBase = ListProductBase(products=[])
            for product in products_data:
                data_result.products.append(
                    ProductBase(
                        id_product=product[0].id,
                        label_product=product[0].label_product,
                        type_pr=[
                            ProductTypeModels(
                                id_moto_type=tp.id_type_model,
                                id_product=tp.id_product,
                            )
                            for tp in product[0].type_models
                        ],
                        article_product=product[0].article_product,
                        title_product=product[0].title_product,
                        brand=product[0].brand,
                        brand_mark=[
                            ProductMarks(
                                id_mark=mark.id_mark,
                                id_product=mark.id_product,
                            )
                            for mark in product[0].brand_mark
                        ],
                        models=[
                            model.read_model()
                            for model in product[0].product_models_data
                        ],
                        id_sub_category=product[0].id_sub_category,
                        weight_product=product[0].weight_product,
                        is_recommended=product[0].is_recommended,
                        explanation_product=product[0].explanation_product,
                        quantity_product=product[0].quantity_product,
                        price_product=product[0].price_product,
                        date_create_product=product[0].date_create_product,
                        date_update_information=product[
                            0
                        ].date_update_information,  # noqa
                        product_discount=product[0].product_discount,
                        photo=(
                            [photo.read_model() for photo in product[0].photos]
                            if product[0].photos
                            else []
                        ),
                    )
                )
            return data_result
        await ProductHttpError().http_product_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_product_discount(
        engine: IEngineRepository,
        token: str,
        id_product: int,
        new_discount: UpdateProductDiscount,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервися для обновления скидки товара
        :session:
        :token:
        :id_product:
        :new_discout:
        """

        logging.info(msg=f"{ProductService.__name__} Обновление скидки товара")

        async with engine:
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                # Обновление скидки товара
                is_updated: bool = await engine.product_repository.update_one(
                    other_id=id_product,
                    data_to_update=new_discount.model_dump(),
                )

                if is_updated:
                    return
                logging.info(
                    msg=f"{ProductService.__name__} "
                    f"Не удалось обновить скидку товара"
                )
                (
                    await ProductHttpError().http_failed_to_update_product_information()  # noqa
                )
            logging.info(
                msg=f"{ProductService.__name__} "
                f"Не удалось обновить скидку товара, "
                f"пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_new_products(
        engine: IEngineRepository, redis_search_data: str
    ) -> Union[List, List[ProductBase]]:
        """
        Получение новых продуктов
        """

        logging.info(
            msg=f"{ProductService.__name__} " f"Получение новых товаров"
        )
        async with engine:
            all_products: Union[None, List[ProductBase]] = (
                await engine.product_repository.get_products_by_date()
            )

            if all_products:

                result: list = []

                for product in all_products:
                    if len(result) >= 7:
                        break
                    result.append(
                        ProductBase(
                            id_product=product[0].id,
                            label_product=product[0].label_product,
                            type_pr=[
                                ProductTypeModels(
                                    id_moto_type=tp.id_type_model,
                                    id_product=tp.id_product,
                                )
                                for tp in product[0].type_models
                            ],
                            article_product=product[0].article_product,
                            title_product=product[0].title_product,
                            brand=product[0].brand,
                            brand_mark=[
                                ProductMarks(
                                    id_mark=mark.id_mark,
                                    id_product=mark.id_product,
                                )
                                for mark in product[0].brand_mark
                            ],
                            models=[
                                model.read_model()
                                for model in product[0].product_models_data
                            ],
                            id_sub_category=product[0].id_sub_category,
                            weight_product=product[0].weight_product,
                            is_recommended=product[0].is_recommended,
                            explanation_product=product[0].explanation_product,
                            quantity_product=product[0].quantity_product,
                            price_product=product[0].price_product,
                            date_create_product=product[0].date_create_product,
                            date_update_information=product[
                                0
                            ].date_update_information,  # noqa
                            product_discount=product[0].product_discount,
                            photo=(
                                [
                                    photo.read_model()
                                    for photo in product[0].photos
                                ]
                                if product[0].photos
                                else []
                            ),
                        )
                    )
                return ListProductBase(products=result)
            await ProductHttpError().http_product_not_found()
