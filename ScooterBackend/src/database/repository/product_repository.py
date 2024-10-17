# System
from typing import List, Union, Type
import logging as logger

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

# Local
from src.database.models.product import Product
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.category import Category


logging = logger.getLogger(__name__)


class ProductRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Product] = Product
        super().__init__(session=session, model=self.model)

    async def del_more(
        self, session: AsyncSession, id_products: List[int]
    ) -> bool:
        """
        Удаление нескольких товаров
        :param args:
        :param kwargs:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Удаление нескольких товаров"
            f" id={id_products}"
        )
        for id_product in id_products:
            delete_product = delete(Product).where(Product.id == id_product)
            await session.execute(delete_product)
            await session.commit()

        return True

    async def find_by_category(
        self, how_to_find: Union[str, int]
    ) -> Union[List, List[Product]]:
        """
        Поиск товаров по категории
        :param session:
        :param how_to_find:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} " f"Поиск товаров по категории"
        )
        if isinstance(how_to_find, int):
            stmt = select(Product).where(Product.id_category == how_to_find)
            all_products = (await self.async_session.execute(stmt)).fetchall()
            return all_products
        elif isinstance(how_to_find, str):
            # Поиск категории
            stmt = select(Category).where(Category.name_category == how_to_find)
            category_data = (
                await self.async_session.execute(stmt)
            ).one_or_none()

            if category_data:
                category_data: Category = category_data[0]

                # Поиск товаров
                stmt = select(Product).where(
                    Product.id_category == category_data.id
                )
                all_products = (
                    await self.async_session.execute(stmt)
                ).fetchall()
                return all_products
            return []

    async def find_product_by_name(
        self, name_product: str
    ) -> Union[None, Product]:
        """
        Поиск продукта по названию.
        :param name_product:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Поиск продукта по"
            f" названию name_product={name_product}"
        )
        stmt = select(Product).where(Product.title_product == name_product)
        product_data = (await self.async_session.execute(stmt)).one_or_none()

        return product_data

    async def get_all_info(self, id_product: int) -> Union[None, Product]:
        """
        Получение всей информации о продукте
        :param id_product:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Получение всей информации"
            f" о продукте id_product={id_product}"
        )
        stmt = (
            select(Product)
            .where(Product.id == id_product)
            .options(
                joinedload(Product.reviews),
                joinedload(Product.product_info_for_fav),
                joinedload(Product.order),
                joinedload(Product.product_all_categories),
            )
        )
        product_data = (
            (await self.async_session.execute(stmt)).unique().one_or_none()
        )

        return product_data

    async def find_by_filters(
        self, id_categories: int, min_price: int, max_price: int, desc: bool
    ) -> Union[List, List[Product]]:
        """
        Поиск всех продуктов по фильтру
        :param id_categories:
        :param min_price:
        :param max_price:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Поиск продуктов по фильтрам"
            f" id_categories={id_categories};"
            f" min_price={min_price};"
            f" max_price={max_price};"
            f" desc={desc}"
        )
        stmt = select(Product).options(
            joinedload(Product.product_all_categories)
        )

        if id_categories:
            stmt = stmt.where(Product.id_category == id_categories)

        if min_price:
            stmt = stmt.filter(Product.price_product >= min_price)
        if max_price:
            stmt = stmt.filter(Product.price_product <= max_price)

        if desc:
            stmt = stmt.order_by(Product.price_product.desc())

        products: Union[List, List[Product]] = (
            (await self.async_session.execute(stmt)).unique().scalars().all()
        )
        return products

    async def get_products_by_date(self) -> Union[None, List[Product]]:
        """
        Получение всех товаров по дате
        :session:
        """

        logging.info(
            msg="{self.__class__.__name__} Получение всех товаров"
            " по новым датам"
        )
        stmt = select(Product).order_by(Product.date_create_product.desc())
        products = (await self.async_session.execute(stmt)).fetchall()

        if products:
            return products
        return None
