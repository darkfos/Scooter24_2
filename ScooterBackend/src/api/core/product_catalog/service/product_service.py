# System
import datetime, logging
from typing import Union, Dict, List, Type, Coroutine, Any
from random import choice

# Other libraries
from fastapi import UploadFile


# Local
from src.database.models.product import Product
from src.api.core.product_catalog.error.http_product_exception import *
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.core.category_catalog.error.http_category_exception import CategoryHttpError
from src.api.core.product_catalog.schemas.product_dto import *
from src.api.authentication.secure.authentication_service import Authentication
from src.api.authentication.hash_service.hashing import CryptographyScooter
from src.api.dep.dependencies import IEngineRepository
from src.other.image.image_saver import ImageSaver


# Redis
from src.store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()


class ProductService:

    @auth
    @staticmethod
    async def create_product(
        engine: IEngineRepository,
        token: str,
        new_product: ProductBase,
        photo_product: UploadFile,
        token_data: dict = dict()
    ) -> ProductIsCreated:
        """
        Метод для создания нового продукта
        :param session:
        :param token:
        :param new_product:
        :return:
        """

        logging.info(msg=f"{ProductService.__name__} Создание нового продукта")

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )
            if is_admin:
                product = Product(
                    title_product=new_product.title_product,
                    price_product=new_product.price_product,
                    quantity_product=new_product.quantity_product,
                    explanation_product=new_product.explanation_product,
                    article_product=new_product.article_product,
                    tags=new_product.tags,
                    other_data=new_product.other_data,
                    photo_product=new_product.photo_product,
                    date_create_product=new_product.date_create_product,
                    date_update_information=new_product.date_update_information,
                    product_discount=new_product.price_discount,
                )
                # Create product
                product_is_created: bool = await engine.product_repository.add_one(
                    data=product
                )

                image_saver: Type[ImageSaver] = ImageSaver()

                if product_is_created:
                    await image_saver.generate_filename(
                        id_=product_is_created, filename=photo_product.filename
                    )

                    # Save file
                    url_save_photo: str = await image_saver.save_file(
                        file=photo_product
                    )

                    if url_save_photo:

                        is_updated: bool = await engine.product_repository.update_one(
                            other_id=product_is_created,
                            data_to_update={"photo_product": url_save_photo},
                        )
                        if is_updated:
                            return ProductIsCreated(
                                is_created=True, product_name=url_save_photo
                            )

                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Не удалось загрузить фотографию продукта",
                    )
            logging.critical(msg=f"{ProductService.__name__} Не удалось создать новый продукт")
            await ProductHttpError().http_failed_to_create_a_new_product()

    @auth
    @staticmethod
    async def add_new_category(
        engine: IEngineRepository, id_product: int, id_category: int, admin_data: str, token_data: dict = dict()
    ) -> None:
        """
        Метод сервиса для добавления новой категории для товара
        :param engine:
        :param id_product:
        :param id_category:
        :param admin_data:
        """

        logging.info(msg=f"{ProductService.__name__} Добавление новой категории для товара")

        async with engine:
            is_admin = await engine.admin_repository.find_admin_by_email_and_password(
                email=token_data.get("email"),
                password=CryptographyScooter().hashed_password(
                    password=token_data.get("password")
                ),
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
                    else await CategoryHttpError().http_failed_to_create_a_new_category()
                )
            logging.critical(msg=f"{ProductService.__name__} Не удалось добавить новую категорию к товару")
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
                            title_product=product[0].title_product,
                            price_product=product[0].price_product,
                            quantity_product=product[0].quantity_product,
                            explanation_product=product[0].explanation_product,
                            article_product=product[0].article_product,
                            tags=product[0].tags,
                            other_data=product[0].other_data,
                            photo_product=f"{product[0].photo_product}",
                            date_create_product=product[0].date_create_product,
                            date_update_information=product[0].date_update_information,
                            price_discount=(
                                product[0].product_discount
                                if product[0].product_discount
                                else 0
                            ),
                        )
                        for product in all_products
                    ]
                )

            return ListProductBase(products=[])

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

        logging.info(msg=f"{ProductService.__name__} Получение списка товаров по категории category_data={category_data}")
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
                            title_product=product[0].title_product,
                            price_product=product[0].price_product,
                            quantity_product=product[0].quantity_product,
                            explanation_product=product[0].explanation_product,
                            article_product=product[0].article_product,
                            tags=product[0].tags,
                            other_data=product[0].other_data,
                            date_create_product=product[0].date_create_product,
                            date_update_information=product[0].date_update_information,
                            photo_product=f"{product[0].photo_product}",
                            price_discount=(
                                product[0].product_discount
                                if product[0].product_discount
                                else 0
                            ),
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

        logging.info(msg=f"{ProductService.__name__} Поиск продукта по id={id_product}")
        async with engine:
            product_data = await engine.product_repository.find_one(other_id=id_product)

            if product_data:
                return ProductBase(
                    title_product=product_data[0].title_product,
                    price_product=product_data[0].price_product,
                    quantity_product=product_data[0].quantity_product,
                    explanation_product=product_data[0].explanation_product,
                    article_product=product_data[0].article_product,
                    tags=product_data[0].tags,
                    other_data=product_data[0].other_data,
                    date_create_product=product_data[0].date_create_product,
                    date_update_information=product_data[0].date_update_information,
                    photo_product=f"{product_data[0].photo_product}",
                    price_discount=(
                        product_data[0].product_discount
                        if product_data[0].product_discount
                        else 0
                    ),
                )
            logging.critical(msg=f"{ProductService.__name__} Не удалось удалить продукт по id={id_product}")
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

        logging.info(msg=f"{ProductService.__name__} Поиск продукта по name={name_product}")
        async with engine:
            product_data: Union[None, Product] = (
                await engine.product_repository.find_product_by_name(
                    name_product=name_product
                )
            )

            if product_data:
                return ProductBase(
                    title_product=product_data[0].title_product,
                    price_product=product_data[0].price_product,
                    quantity_product=product_data[0].quantity_product,
                    explanation_product=product_data[0].explanation_product,
                    article_product=product_data[0].article_product,
                    tags=product_data[0].tags,
                    other_data=product_data[0].other_data,
                    date_create_product=product_data[0].date_create_product,
                    date_update_information=product_data[0].date_update_information,
                    photo_product=f"{product_data[0].photo_product}",
                    price_discount=(
                        product_data[0].product_discount
                        if product_data[0].product_discount
                        else 0
                    ),
                )
            
            logging.critical(msg=f"{ProductService.__name__} Не удалось найти продукт")
            await ProductHttpError().http_product_not_found()

    @staticmethod
    async def product_is_created(engine: IEngineRepository, product_name: str) -> None:
        """
        Метод сервиса для проверки что продукт существует
        :param session:
        :param product_name:
        :return:
        """

        logging.info(msg=f"{ProductService.__name__} Проверка существования продукта")
        async with engine:
            product_is_created = await engine.product_repository.find_product_by_name(
                name_product=product_name
            )

            if product_is_created:
                return True
            logging.critical(msg=f"{ProductService.__name__} Не удалось найти продукт")
            await ProductHttpError().http_product_not_found()

    @auth
    @redis
    @staticmethod
    async def get_all_information_about_product(
        engine: IEngineRepository, token: str, id_product: int, redis_search_data: str, token_data: dict = dict()
    ) -> ProductAllInformation:
        """
        Метод сервиса для получения полной информации о продукте
        :param session:
        :param token:
        :return:
        """

        logging.info(msg=f"{ProductService.__name__} Получение полной информации о продукте")

        async with engine:
            # Is admin
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                product_data: Union[None, Product] = (
                    await engine.product_repository.get_all_info(id_product=id_product)
                )
                if product_data:
                    return ProductAllInformation(
                        title_product=product_data[0].title_product,
                        price_product=product_data[0].price_product,
                        quantity_product=product_data[0].quantity_product,
                        explanation_product=product_data[0].explanation_product,
                        article_product=product_data[0].article_product,
                        tags=product_data[0].tags,
                        other_data=product_data[0].other_data,
                        date_create_product=product_data[0].date_create_product,
                        date_update_information=product_data[0].date_update_information,
                        photo_product=f"{product_data[0].photo_product}",
                        price_discount=(
                            product_data[0].product_discount
                            if product_data[0].product_discount
                            else 0
                        ),
                        reviews=[
                            review_p.read_model()
                            for review_p in product_data[0].reviews
                        ],
                        orders=[
                            order_pr.read_model() for order_pr in product_data[0].order
                        ],
                        favourites=[
                            fav_p.read_model()
                            for fav_p in product_data[0].product_info_for_fav
                        ],
                        categories=[
                            cat_data.read_model()
                            for cat_data in product_data[0].product_all_categories
                        ],
                    )
                logging.critical(msg=f"{ProductService.__name__} Не удалось найти продукт")
                await ProductHttpError().http_product_not_found()
            logging.critical(msg=f"{ProductService.__name__} Не удалось найти продукт, пользователь не был найден")
            await UserHttpError().http_user_not_found()

    @auth
    @staticmethod
    async def update_information(
        engine: IEngineRepository,
        id_product: int,
        token: str,
        data_to_update: UpdateProduct,
        token_data: dict = dict()
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
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                # Update data
                is_updated: bool = await engine.product_repository.update_one(
                    other_id=id_product, data_to_update=data_to_update.model_dump()
                )

                if is_updated:
                    return
                logging.critical(msg=f"{ProductService.__name__} Не удалось обновить продукт, продукт не был найден")
                await ProductHttpError().http_failed_to_update_product_information()
            logging.critical(msg=f"{ProductService.__name__} Не удалось обновить продукт, пользователь не был найден")
            await UserHttpError().http_user_not_found()

    @auth
    @staticmethod
    async def update_photo(
        engine: IEngineRepository, token: str, photo_data: str, product_id: int, token_data: dict = dict()
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
            logging.critical(msg=f"{ProductService.__name__} Не удалось обновить фотографию")
            await UserHttpError().http_user_not_found()

    @auth
    @staticmethod
    async def delete_product_by_id(
        engine: IEngineRepository, token: str, id_product: int, token_data: dict = dict()
    ) -> None:
        """
        Метод сервиса для удаления продукта по id
        :param session:
        :param token:
        :param id_product:
        :return:
        """

        logging.info(msg=f"{ProductService.__name__} Удаление продукта по id = {id_product}")

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                product_data: Product = await engine.product_repository.find_one(
                    other_id=id_product
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
                logging.critical(msg=f"{ProductService.__name__} Не удалось удалить продукт по id = {id_product}")
                await ProductHttpError().http_failed_to_delete_product()
            logging.info(msg=f"{ProductService.__name__} Не удалось удалить продукт по id = {id_product}, пользователь не был найден")
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_products_by_sorted(
        engine: IEngineRepository,
        desc: bool,
        redis_search_data: str,
        sorted_by_category: int = None,
        sorted_by_price_min: int = None,
        sorted_by_price_max: int = None,
    ) -> ListProductBase:
        """
        Метод сервиса для поиска товаров, а также их сортировки
        :param session:
        :param token:
        :param id_product:
        :return:
        """

        logging.info(msg=f"{ProductService.__name__} Поиск продуктов по требованиям desc={desc}, category={sorted_by_category}, min_price={sorted_by_price_min}, max_price={sorted_by_price_max}")

        async with engine:
            # Получаем товары
            products: Union[List, List[ProductBase]] = (
                await engine.product_repository.find_by_filters(
                    id_categories=sorted_by_category,
                    min_price=sorted_by_price_min,
                    max_price=sorted_by_price_max,
                    desc=desc,
                )
            )

            if products:
                return ListProductBase(
                    products=[
                        ProductBase(
                            title_product=product.title_product,
                            price_product=product.price_product,
                            quantity_product=product.quantity_product,
                            explanation_product=product.explanation_product,
                            article_product=product.article_product,
                            tags=product.tags,
                            other_data=product.other_data,
                            photo_product=product.photo_product,
                            price_discount=(
                                product.product_discount
                                if product.product_discount
                                else 0
                            ),
                        )
                        for product in products
                    ]
                )
            return ListProductBase(products=[])

    @redis
    @staticmethod
    async def get_recommended_products(
        engine: IEngineRepository, redis_search_data: str
    ) -> Union[List, List[ProductBase]]:
        """
        Метод сервиса для получения рекомендованных товаров.
        :session:
        """

        logging.info(msg=f"{ProductService.__name__} Получение рекомендованных товаров")

        async with engine:
            # Получение всех товаров
            all_products: Union[List, List[Product]] = (
                await engine.product_repository.find_all()
            )

            if all_products:

                result: list = []

                while len(result) != 7:

                    rnd_product: Product = choice(all_products)
                    result.append(
                        ProductBase(
                            title_product=rnd_product[0].title_product,
                            price_product=rnd_product[0].price_product,
                            quantity_product=rnd_product[0].quantity_product,
                            explanation_product=rnd_product[0].explanation_product,
                            article_product=rnd_product[0].article_product,
                            tags=rnd_product[0].tags,
                            other_data=rnd_product[0].other_data,
                            photo_product=rnd_product[0].photo_product,
                            date_create_product=rnd_product[0].date_create_product,
                            date_update_information=rnd_product[
                                0
                            ].date_update_information,
                            price_discount=(
                                rnd_product[0].product_discount
                                if rnd_product[0].product_discount
                                else 0
                            ),
                        )
                    )

                    if len(all_products) < 7:
                        break

                return ListProductBase(products=[*result])

            return []

    @staticmethod
    async def update_product_discount(
        engine: IEngineRepository,
        token: str,
        id_product: int,
        new_discount: UpdateProductDiscount,
    ) -> None:
        """
        Метод сервися для обновления скидки товара
        :session:
        :token:
        :id_product:
        :new_discout:
        """

        logging.info(msg=f"{ProductService.__name__} Обновление скидки товара")

        # Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(
            token=token, type_token="access"
        )

        async with engine:
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=jwt_data.get("email")
                )
            )

            if is_admin:
                # Обновление скидки товара
                is_updated: bool = await engine.product_repository.update_one(
                    other_id=id_product, data_to_update=new_discount.model_dump()
                )

                if is_updated:
                    return
                
                logging.info(msg=f"{ProductService.__name__} Не удалось обновить скидку товара")
                await ProductHttpError().http_failed_to_update_product_information()
            logging.info(msg=f"{ProductService.__name__} Не удалось обновить скидку товара, пользователь не был найден")
            await UserHttpError().http_user_not_found()

    # TODO: Refactor
    @redis
    @staticmethod
    async def get_new_products(
        engine: IEngineRepository, redis_search_data: str
    ) -> Union[List, List[ProductBase]]:
        """
        Получение новых продуктов
        """

        logging.info(msg=f"{ProductService.__name__} Получение новых товаров")
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
                            title_product=product[0].title_product,
                            price_product=product[0].price_product,
                            quantity_product=product[0].quantity_product,
                            explanation_product=product[0].explanation_product,
                            article_product=product[0].article_product,
                            tags=product[0].tags,
                            other_data=product[0].other_data,
                            photo_product=product[0].photo_product,
                            date_create_product=product[0].date_create_product,
                            date_update_information=product[0].date_update_information,
                            price_discount=(
                                product[0].product_discount
                                if product[0].product_discount
                                else 0
                            ),
                        )
                    )

                return ListProductBase(products=[*result])

            return ListProductBase(products=[])
