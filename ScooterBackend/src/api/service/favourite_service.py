#System
from typing import List, Dict, Union

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from src.api.authentication.authentication_service import Authentication
from src.api.exception.http_favourite_exception import FavouriteHttpError
from src.api.exception.http_user_exception import UserHttpError
from src.database.models.favourite import Favourite
from src.database.repository.favourite_repository import FavouriteRepository
from src.database.repository.admin_repository import AdminRepository
from src.api.dto.favourite_dto import *
from src.api.dep.dependencies import IEngineRepository, EngineRepository


class FavouriteService:

    @staticmethod
    async def create_favourite_product(
        engine: IEngineRepository,
        token: str,
        new_product_in_favourite: AddFavourite
    ) -> None:
        """
        Добавление нового товара в избранное
        :param session:
        :param token:
        :param new_product_in_favourite:
        :return:
        """

        #Получаем данные из токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на добавление в избранное
            is_created: bool = await engine.favourite_repository.add_one(
                data=Favourite(
                    id_user=jwt_data.get("id_user"),
                    id_product=new_product_in_favourite.id_product
                )
            )

            if is_created:
                return

            await FavouriteHttpError().http_failed_to_create_a_new_favourite()

    @staticmethod
    async def get_all_favourite_product_by_user_id(engine: IEngineRepository, token: str) -> FavouriteBase:
        """
        Список всех избранных товаров пользователя.
        :param session:
        :param token:
        :param id_user:
        :return:
        """

        #Получаем данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Получаем список товаров
            all_favourite_products: Union[List, List[Favourite]] = await engine.favourite_repository.get_all_data_for_id_user(id_user=jwt_data.get("id_user"))

            if all_favourite_products:
                product_data: List[FavouriteBase] = []
                for product in all_favourite_products:
                    product_data.append(
                        FavouriteBase(
                            product_info={
                                "product_name": product.product_info.title_product,
                                "price_product": product.product_info.price_product,
                                "article_product": product.product_info.article_product,
                                "tags": product.product_info.tags}
                        )
                    )

                return product_data

            return all_favourite_products

    @staticmethod
    async def get_information_about_fav_product_by_id(
        engine: IEngineRepository,
        token: str,
        id_fav_product: int
    ) -> FavouriteInformation:
        """
        Метод сервиса для получение полной информации о избранном товаре
        :param session:
        :param token:
        :param id_fav_product:
        :return:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if is_admin:
                find_favourite_product: Union[Favourite, None] = \
                    await engine.favourite_repository.get_all_data_for_favourite_product_by_id(id_fav_product=id_fav_product)

                if find_favourite_product:
                    return FavouriteInformation(
                        product_info={
                            "name_product": find_favourite_product.product_info.title_product,
                            "price_product": find_favourite_product.product_info.price_product,
                            "description": find_favourite_product.product_info.explanation_product,
                            "id_category": find_favourite_product.product_info.id_category
                        },
                        user_detail_information={
                            "email_user": find_favourite_product.fav_user.email_user,
                            "name_user": find_favourite_product.fav_user.name_user
                        },
                    )

                await FavouriteHttpError().http_favourite_not_found()

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_all_favourites(
        engine: IEngineRepository,
        token: str
    ) -> Union[List, List[FavouriteSmallData]]:
        """
        Получение всех избранных товаров
        :param session:
        :param token:
        :return:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(email=jwt_data.get("email"))

            if is_admin:
                all_fav: Union[List, List[Favourite]] =  await engine.favourite_repository.find_all()
                if all_fav:
                    all_fav_products: List[FavouriteSmallData] = list()

                    for fav in all_fav[0]:
                        all_fav_products.append(
                            FavouriteSmallData(
                                id_fav=fav.id,
                                id_product=fav.id_product,
                                id_user=fav.id_user
                            )
                        )

                    return all_fav_products
                return []

            await UserHttpError().http_user_not_found()

    @staticmethod
    async def delete_favourite_product(
        engine: IEngineRepository,
        token: str,
        id_favourite: int
    ) -> None:
        """
        Метод сервиса для удаление товара из списка избранных.
        :param session:
        :param token:
        :param id_favourite:
        :return:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на пользователя
            get_favourite_data: Union[None, Favourite] = await engine.favourite_repository.find_one(other_id=id_favourite)

            if get_favourite_data:
                get_favourite_data = get_favourite_data[0]

                if get_favourite_data.id_user == jwt_data.get("id_user"):
                    is_deleted: bool = await engine.favourite_repository.delete_one(other_id=id_favourite)
                    if is_deleted: return
                    await FavouriteHttpError().http_failed_to_delete_favourite()
                await UserHttpError().http_user_not_found()
            await FavouriteHttpError().http_favourite_not_found()