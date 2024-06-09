#System
from typing import List, Union, Type

#Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, Result
from sqlalchemy.orm import joinedload

#Local
from ScooterBackend.database.models.product import Product
from ScooterBackend.database.repository.general_repository import GeneralSQLRepository
from ScooterBackend.database.models.category import Category


class ProductRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Product = Product
        super().__init__(session=session, model=self.model)

    async def del_more(self, session: AsyncSession, id_products: List[int]) -> bool:
        """
        Удаление нескольких товаров
        :param args:
        :param kwargs:
        :return:
        """

        for id_product in id_products:
            delete_product = delete(Product).where(Product.id == id_product)
            await session.execute(delete_product)
            await session.commit()

        return True

    async def find_by_category(self, how_to_find: Union[str, int]) -> Union[List, List[Product]]:
        """
        Поиск товаров по категории
        :param session:
        :param how_to_find:
        :return:
        """

        if isinstance(how_to_find, int):
            stmt = select(Product).where(Product.id_category == how_to_find)
            all_products = (await self.async_session.execute(stmt)).fetchall()
            return all_products
        elif isinstance(how_to_find, str):
            #Поиск категории
            stmt = select(Category).where(Category.name_category == how_to_find)
            category_data = (await self.async_session.execute(stmt)).one_or_none()

            if category_data:
                category_data: Category = category_data[0]

                #Поиск товаров
                stmt = select(Product).where(Product.id_category == category_data.id)
                all_products = (await self.async_session.execute(stmt)).fetchall()
                return all_products
            return []

    async def find_product_by_name(self, name_product: str) -> Union[None, Product]:
        """
        Поиск продукта по названи.
        :param name_product:
        :return:
        """

        stmt = select(Product).where(Product.title_product == name_product)
        product_data = (await self.async_session.execute(stmt)).one_or_none()

        return product_data

    async def get_all_info(self, id_product: int) -> Union[None, Product]:
        """
        Получение всей информации о продукте
        :param id_product:
        :return:
        """

        stmt = select(Product).where(Product.id == id_product).options(
            joinedload(Product.reviews),
            joinedload(Product.product_info_for_fav),
            joinedload(Product.category),
            joinedload(Product.order)
        )
        product_data = ((await self.async_session.execute(stmt)).unique()).one_or_none()

        return product_data