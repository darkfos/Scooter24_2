#System
import datetime
from typing import Union, Dict, List
from random import choice

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile


#Local
from database.models.product import Product
from api.exception.http_product_exception import *
from api.exception.http_user_exception import UserHttpError
from api.dto.product_dto import *
from api.authentication.authentication_service import Authentication
from database.repository.product_repository import ProductRepository
from database.repository.admin_repository import AdminRepository
from api.dep.dependencies import IEngineRepository


class ProductService:

    @staticmethod
    async def create_product(
        engine: IEngineRepository,
        token: str,
        new_product: ProductBase,
    ) -> ProductIsCreated:
        """
        Метод для создания нового продукта
        :param session:
        :param token:
        :param new_product:
        :return:
        """

        #Getting token data
        jwt_data: Dict[str, Union[int, str]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))
            if is_admin:
                product = Product(
                    title_product=new_product.title_product,
                    price_product=new_product.price_product,
                    quantity_product=new_product.quantity_product,
                    explanation_product=new_product.explanation_product,
                    article_product=new_product.article_product,
                    tags=new_product.tags,
                    other_data=new_product.other_data,
                    id_category=new_product.id_category,
                    photo_product=new_product.photo_product,
                    date_create_product=new_product.date_create_product,
                    date_update_information=new_product.date_update_information,
                    product_discount=new_product.price_discount
                )
                #Create product
                product_is_created: bool = await (engine.product_repository.add_one(
                    data=product
                ))
                if product_is_created:
                    is_updated: bool = await engine.product_repository.update_one(
                               other_id=product_is_created,
                                data_to_update={"photo_product": (str(product_is_created)+"_"+product.photo_product)}
                            )
                    if is_updated:
                        return ProductIsCreated(
                            is_created=True,
                            product_name=str(product_is_created)+"_"+product.photo_product
                        )

            await ProductHttpError().http_failed_to_create_a_new_product()

    @staticmethod
    async def get_all_products(
        engine: IEngineRepository
    ) -> List[ProductBase]:
        """
        Метод сервиса для получения всех товаров
        :param session:
        :return:
        """

        async with engine:
            all_products = await engine.product_repository.find_all()

            if all_products:
                return [
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
                        id_category=product[0].id_category,
                        price_discount=product[0].product_discount if product[0].product_discount else 0
                )
                    for product in all_products
                ]

            return []

    @staticmethod
    async def get_products_by_category(engine: IEngineRepository, category_data: Union[str, int]) -> Union[List, List[ProductBase]]:
        """
        Метод сервиса для получения списка товаров по категории
        :param session:
        :param category_data:
        :return:
        """

        async with engine:
            all_products: Union[List, List[Product]] = await engine.product_repository.find_by_category(
                how_to_find=category_data if not category_data.isdigit() else int(category_data)
            )

            if all_products:
                return [
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
                        id_category=product[0].id_category,
                        price_discount=product[0].product_discount if product[0].product_discount else 0
                    )
                    for product in all_products
                ]

            return []

    @staticmethod
    async def find_product_by_id(engine: IEngineRepository, id_product: int) -> ProductBase:
        """
        Метод сервиса для поиска продукта по id
        :param session:
        :param id_product:
        :return:
        """

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
                    id_category=product_data[0].id_category,
                    price_discount=product_data[0].product_discount if product_data[0].product_discount else 0
                )

            await ProductHttpError().http_product_not_found()

    @staticmethod
    async def find_product_by_name(engine: IEngineRepository, name_product: str) -> ProductBase:
        """
        Метод сервиса для поиска продукта по названию
        :param session:
        :param name_product:
        :return:
        """

        async with engine:
            product_data: Union[None, Product] = await engine.product_repository.find_product_by_name(
                name_product=name_product)

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
                    id_category=product_data[0].id_category,
                    price_discount=product_data[0].product_discount if product_data[0].product_discount else 0
                )

            await ProductHttpError().http_product_not_found()

    @staticmethod
    async def product_is_created(engine: IEngineRepository, product_name: str) -> None:
        """
        Метод сервиса для проверки что продукт существует
        :param session:
        :param product_name:
        :return:
        """

        async with engine:
            product_is_created = await engine.product_repository.find_product_by_name(name_product=product_name)

            if product_is_created:
                return
            await ProductHttpError().http_product_not_found()

    @staticmethod
    async def get_all_information_about_product(engine: IEngineRepository, token: str, id_product: int) -> ProductAllInformation:
        """
        Метод сервиса для получения полной информации о продукте
        :param session:
        :param token:
        :return:
        """

        #Get data from token
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Is admin
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if is_admin:
                product_data: Union[None, Product] = await engine.product_repository.get_all_info(id_product=id_product)
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
                        id_category=product_data[0].id_category,
                        price_discount=product_data[0].product_discount if product_data[0].product_discount else 0,
                        reviews=[
                            review_p.read_model()
                            for review_p in product_data[0].reviews
                        ],
                        category_data=[product_data[0].category.read_model()],
                        orders=[
                            order_pr.read_model()
                            for order_pr in product_data[0].order
                        ],
                        favourites=[
                            fav_p.read_model()
                            for fav_p in product_data[0].product_info_for_fav
                        ]
                    )

                await ProductHttpError().http_product_not_found()

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def update_information(
        engine: IEngineRepository,
        id_product: int,
        token: str,
        data_to_update: UpdateProduct
    ) -> None:
        """
        Метод сервиса для обновления информации о продукте
        :param session:
        :param id_product:
        :param token:
        :param data_to_update:
        :return:
        """

        #Getting jwt data
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Is admin
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if is_admin:
                #Update data
                is_updated: bool = await engine.product_repository.update_one(
                    other_id=id_product,
                    data_to_update=data_to_update.model_dump()
                )

                if is_updated:
                    return
                await ProductHttpError().http_failed_to_update_product_information()

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def update_photo(engine: IEngineRepository, token: str, photo_data: str, product_id: int) -> None:
        """
        Метод сервиса для обновления фотографии товара
        :param session:
        :param token:
        :param photo_data:
        :return:
        """

        #Getting data from token
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if is_admin:
                #Обновление фотографии
                await engine.product_repository.update_one(other_id=product_id, data_to_update={
                    "photo_product": str(product_id)+"_"+photo_data, "date_update_information": datetime.date.today()})
                return

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def delete_product_by_id(
        engine: IEngineRepository,
        token: str,
        id_product: int
    ) -> None:
        """
        Метод сервиса для удаления продукта по id
        :param session:
        :param token:
        :param id_product:
        :return:
        """

        #Getting data from token
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if is_admin:
                is_del: bool = await engine.product_repository.delete_one(other_id=id_product)

                if is_del:
                    return

                await ProductHttpError().http_failed_to_delete_product()

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_products_by_sorted(
        engine: IEngineRepository,
        desc: bool,
        sorted_by_category: int = None,
        sorted_by_price_min: int = None,
        sorted_by_price_max: int = None,
    ) -> List[ProductBase]:
        """
        Метод сервиса для поиска товаров, а также их сортировки
        :param session:
        :param token:
        :param id_product:
        :return:
        """

        async with engine:
            #Получаем товары
            products: Union[List, List[ProductBase]] = await engine.product_repository.find_by_filters(
                id_categories=sorted_by_category,
                min_price=sorted_by_price_min,
                max_price=sorted_by_price_max,
                desc=desc
            )

            if products:
                return [
                    ProductBase(
                        title_product=product.title_product,
                        price_product=product.price_product,
                        quantity_product=product.quantity_product,
                        explanation_product=product.explanation_product,
                        article_product=product.article_product,
                        tags=product.tags,
                        other_data=product.other_data,
                        photo_product=product.photo_product,
                        id_category=product.id_category,
                        price_discount=product.product_discount if product.product_discount else 0
                    )
                    for product in products
                ]

            return []

    @staticmethod
    async def get_recommended_products(
        engine: IEngineRepository
    ) -> Union[List, List[ProductBase]]:
        """
        Метод сервиса для получения рекомендованных товаров.
        :session:
        """

        async with engine:
            #Получение всех товаров
            all_products: Union[List, List[Product]] = await engine.product_repository.find_all()

            if all_products:

                result: List[ProductBase] = []

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
                            id_category=rnd_product[0].id_category,
                            photo_product=rnd_product[0].photo_product,
                            date_create_product=rnd_product[0].date_create_product,
                            date_update_information=rnd_product[0].date_update_information,
                            price_discount=rnd_product[0].product_discount if rnd_product[0].product_discount else 0
                        )
                    )

                    if len(all_products) < 7:
                        break

                return result

            return []

    @staticmethod
    async def update_product_discount(
        engine: IEngineRepository,
        token: str,
        id_product: int,
        new_discount: UpdateProductDiscount
    ) -> None:
        """
        Метод сервися для обновления скидки товара
        :session:
        :token:
        :id_product:
        :new_discout:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if is_admin:
                #Обновление скидки товара
                is_updated: bool = await engine.product_repository.update_one(
                    other_id=id_product,
                    data_to_update=new_discount.model_dump()
                )

                if is_updated:
                    return

                await ProductHttpError().http_failed_to_update_product_information()

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_new_products(engine: IEngineRepository) -> Union[List, List[ProductBase]]:
        """
        Получение новых продуктов
        """

        async with engine:
            all_products: Union[None, List[ProductBase]] = await engine.product_repository.get_products_by_date()

            if all_products:

                result: List[ProductBase] = []

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
                            id_category=product[0].id_category,
                            photo_product=product[0].photo_product,
                            date_create_product=product[0].date_create_product,
                            date_update_information=product[0].date_update_information,
                            price_discount=product[0].product_discount if product[0].product_discount else 0
                        )
                    )

                return result

            return []