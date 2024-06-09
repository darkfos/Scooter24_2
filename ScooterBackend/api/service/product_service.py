#System
from typing import Union, Dict, List

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile


#Local
from ScooterBackend.database.models.product import Product
from ScooterBackend.api.exception.http_product_exception import *
from ScooterBackend.api.exception.http_user_exception import UserHttpError
from ScooterBackend.api.dto.product_dto import *
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.database.repository.product_repository import ProductRepository
from ScooterBackend.database.repository.admin_repository import AdminRepository


class ProductService:

    @staticmethod
    async def create_product(
        session: AsyncSession,
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

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(email=jwt_data.get("email"))
        if is_admin:
            product = Product(
                title_product=new_product.title_product,
                price_product=new_product.price_product,
                quantity_product=new_product.quantity_product,
                explanation_product=new_product.explanation_product,
                article_product=new_product.article_product,
                tags=new_product.tags,
                other_data=new_product.other_data,
                id_category=new_product.id_category
            )
            #Create product
            product_is_created: bool = await (ProductRepository(session=session).add_one(
                data=product
            ))

            return ProductIsCreated(
                is_created=product_is_created
            )

        await ProductHttpError().http_failed_to_create_a_new_product()

    @staticmethod
    async def get_all_products(
        session: AsyncSession
    ) -> List[ProductBase]:
        """
        Метод сервиса для получения всех товаров
        :param session:
        :return:
        """

        all_products = await ProductRepository(session=session).find_all()

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
                    id_category=product[0].id_category
            )
                for product in all_products
            ]

        return []

    @staticmethod
    async def get_products_by_category(session: AsyncSession, category_data: Union[str, int]) -> Union[List, List[ProductBase]]:
        """
        Метод сервиса для получения списка товаров по категории
        :param session:
        :param category_data:
        :return:
        """

        all_products: Union[List, List[Product]] = await ProductRepository(session=session).find_by_category(
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
                    photo_product=f"{product[0].photo_product}",
                    id_category=product[0].id_category
                )
                for product in all_products
            ]

        return []

    @staticmethod
    async def find_product_by_id(session: AsyncSession, id_product: int) -> ProductBase:
        """
        Метод сервиса для поиска продукта по id
        :param session:
        :param id_product:
        :return:
        """

        product_data = await ProductRepository(session=session).find_one(other_id=id_product)

        if product_data:
            return ProductBase(
                title_product=product_data[0].title_product,
                price_product=product_data[0].price_product,
                quantity_product=product_data[0].quantity_product,
                explanation_product=product_data[0].explanation_product,
                article_product=product_data[0].article_product,
                tags=product_data[0].tags,
                other_data=product_data[0].other_data,
                photo_product=f"{product_data[0].photo_product}",
                id_category=product_data[0].id_category
            )

        await ProductHttpError().http_product_not_found()

    @staticmethod
    async def find_product_by_name(session: AsyncSession, name_product: str) -> ProductBase:
        """
        Метод сервиса для поиска продукта по названию
        :param session:
        :param name_product:
        :return:
        """

        product_data: Union[None, Product] = await ProductRepository(session=session).find_product_by_name(
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
                photo_product=f"{product_data[0].photo_product}",
                id_category=product_data[0].id_category
            )

        await ProductHttpError().http_product_not_found()

    @staticmethod
    async def product_is_created(session: AsyncSession, product_name: str) -> None:
        """
        Метод сервиса для проверки что продукт существует
        :param session:
        :param product_name:
        :return:
        """

        product_is_created = await ProductRepository(session=session).find_product_by_name(name_product=product_name)

        if product_name:
            return
        await ProductHttpError().http_product_not_found()

    @staticmethod
    async def get_all_information_about_product(session: AsyncSession, token: str, id_product: int) -> ProductAllInformation:
        """
        Метод сервиса для получения полной информации о продукте
        :param session:
        :param token:
        :return:
        """

        #Get data from token
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Is admin
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(email=jwt_data.get("email"))

        if is_admin:
            product_data: Union[None, Product] = await ProductRepository(session=session).get_all_info(id_product=id_product)
            if product_data:
                return ProductAllInformation(
                    title_product=product_data[0].title_product,
                    price_product=product_data[0].price_product,
                    quantity_product=product_data[0].quantity_product,
                    explanation_product=product_data[0].explanation_product,
                    article_product=product_data[0].article_product,
                    tags=product_data[0].tags,
                    other_data=product_data[0].other_data,
                    photo_product=f"{product_data[0].photo_product}",
                    id_category=product_data[0].id_category,
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
        session: AsyncSession,
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

        #Is admin
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(email=jwt_data.get("email"))

        if is_admin:
            #Update data
            is_updated: bool = await ProductRepository(session=session).update_one(
                other_id=id_product,
                data_to_update=data_to_update.model_dump()
            )

            if is_updated:
                return
            await ProductHttpError().http_failed_to_update_product_information()

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def update_photo(session: AsyncSession, token: str, photo_data: UploadFile, product_id: int) -> None:
        """
        Метод сервиса для обновления фотографии товара
        :param session:
        :param token:
        :param photo_data:
        :return:
        """

        #Getting data from token
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(email=jwt_data.get("email"))

        if is_admin:
            #Обновление фотографии
            await ProductRepository(session=session).update_one(other_id=product_id, data_to_update={
                "photo_product": photo_data.file.read()})
            return

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def delete_product_by_id(
        session: AsyncSession,
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

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(email=jwt_data.get("email"))

        if is_admin:
            is_del: bool = await ProductRepository(session=session).delete_one(other_id=id_product)

            if is_del:
                return

            await ProductHttpError().http_failed_to_delete_product()

        await UserHttpError().http_user_not_found()