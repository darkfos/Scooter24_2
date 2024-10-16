# System
from typing import Union, List, Type
import logging as logger

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, Result
from sqlalchemy.orm import joinedload

# Local
from src.database.models.favourite import Favourite
from src.database.repository.general_repository import GeneralSQLRepository


logging = logger.getLogger(__name__)


class FavouriteRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Favourite] = Favourite
        super().__init__(session=session, model=self.model)

    async def del_more(
            self,
            id_favourites: List[int]
    ) -> bool:
        """
        Удаление нескольких избранных товаров
        :param args:
        :param kwargs:
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} "
                         f"Осуществлён процесс удаления"
                         f" избранных товаров "
                         f"id_favourites={id_favourites}")

        for id_fav in id_favourites:
            del_favourite: Result = delete(Favourite).where(
                Favourite.id == id_fav
            )
            await self.async_session.execute(del_favourite)
            await self.async_session.commit()

        return True

    async def get_all_data_for_id_user(
        self, id_user: int
    ) -> Union[List, List[Favourite]]:
        """
        Список избранных товаров
        :param id_user:
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} "
                         f"Осуществлён процесс получения"
                         f" списка избранных товаров"
                         f" по id_user=%s" % id_user)

        stmt = (
            select(Favourite)
            .where(Favourite.id_user == id_user)
            .options(
                joinedload(Favourite.fav_user),
                joinedload(Favourite.product_info)
            )
        )

        all_data_products = (
            (await self.async_session.execute(stmt)).unique()
        ).fetchall()

        if all_data_products:
            return all_data_products[0]
        return all_data_products

    async def get_all_data_for_favourite_product_by_id(
        self, id_fav_product: int
    ) -> Union[None, Favourite]:
        """
        Получение полной информации о избранном товаре
        :param id_fav_product:
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} "
                         f"Осуществлён процесс получения"
                         f" полной информации о избранном"
                         f" товаре по id = %s" % id_fav_product)
        stmt = (
            select(Favourite)
            .where(Favourite.id == id_fav_product)
            .options(
                joinedload(Favourite.fav_user),
                joinedload(Favourite.product_info)
            )
        )
        data_favourite_product = (
            (await self.async_session.execute(stmt)).unique()
        ).one_or_none()

        if data_favourite_product:
            return data_favourite_product[0]
        return data_favourite_product
