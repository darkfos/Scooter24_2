# System
from typing import List, Union, Type
import logging as logger

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

# Local
from src.database.models.product import Product
from src.database.models.product_marks import ProductMarks
from src.database.models.product_models import ProductModels
from src.database.models.subcategory import SubCategory
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.product_type_models import ProductTypeModels
from src.other.enums.product_enum import FilteredDescProduct

logging = logger.getLogger(__name__)


class ProductRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Product] = Product
        super().__init__(session=session, model=self.model)

    async def del_more(self, session: AsyncSession, id_products: List[int]) -> bool:
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

        logging.info(msg=f"{self.__class__.__name__} " f"Поиск товаров по категории")
        if isinstance(how_to_find, int):
            stmt = (
                select(Product)
                .where(Product.id_sub_category == how_to_find)
                .options(
                    joinedload(Product.photos),
                    joinedload(Product.brand_mark),
                    joinedload(Product.type_models),
                    joinedload(Product.product_models_data),
                )
            )

            all_products = (await self.async_session.execute(stmt)).unique()
            return all_products.all()

        elif isinstance(how_to_find, str):
            # Поиск товаров
            stmt = (
                select(Product)
                .where(Product.sub_category_data.has(SubCategory.name == how_to_find))
                .options(
                    joinedload(Product.photos),
                    joinedload(Product.brand_mark),
                    joinedload(Product.type_models),
                    joinedload(Product.product_models_data),
                )
            )
            all_products = (await self.async_session.execute(stmt)).fetchall()

            return all_products

        return []

    async def find_product_by_name(self, name_product: str) -> Union[None, Product]:
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
        stmt = select(Product).where(Product.title_product.contains(name_product))
        product_data = (await self.async_session.execute(stmt)).all()

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
                joinedload(Product.sub_category_data),
                joinedload(Product.product_models_data),
                joinedload(Product.photos),
                joinedload(Product.brand_mark),
                joinedload(Product.type_models),
            )
        )
        product_data = (await self.async_session.execute(stmt)).unique().one_or_none()

        return product_data

    async def find_to_garage(
        self,
        id_brand: int = None,
        id_model: int = None,
        id_moto_type: int = None,
    ) -> Union[List, List[Product]]:
        """
        Поиск всех продуктов для гаража по модели и бренду
        """

        logging.info(
            msg=f"{self.__class__.__name__} Поиск продуктов по фильтрам BRAND: {id_brand}; MODEL: {id_model}"  # noqa
        )

        stmt = select(Product).options(
            joinedload(Product.photos),
            joinedload(Product.type_models),
            joinedload(Product.product_models_data),
            joinedload(Product.brand_mark),
            joinedload(Product.photos),
        )

        if id_model:
            stmt = stmt.join(
                ProductModels, ProductModels.id_product == Product.id
            ).where(ProductModels.id_model == id_model)

        if id_brand:
            stmt = stmt.join(ProductMarks, ProductMarks.id_product == Product.id).where(
                ProductMarks.id_mark == id_brand
            )

        if id_moto_type:
            stmt = stmt.join(
                ProductTypeModels, ProductTypeModels.id_product == Product.id
            ).where(ProductTypeModels.id_type_model == id_moto_type)

        result = (await self.async_session.execute(stmt)).unique().all()
        return result

    async def find_by_filters(  # noqa
        self,
        id_categories: int,
        id_sub_category: int,
        min_price: int,
        max_price: int,
        desc: FilteredDescProduct,
        title_product: str,
        availability: bool,
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
            joinedload(Product.sub_category_data),
            joinedload(Product.product_models_data),
            joinedload(Product.photos),
            joinedload(Product.sub_category_data),
            joinedload(Product.brand_mark),
            joinedload(Product.type_models),
        )

        if title_product:
            stmt = stmt.filter(Product.title_product.contains(title_product))

        if id_categories:
            stmt = stmt.filter(
                Product.sub_category_data.has(SubCategory.id_category == id_categories)
            )

        if id_sub_category:
            stmt = stmt.filter(Product.id_sub_category == id_sub_category)

        if min_price:
            stmt = stmt.filter(Product.price_product >= min_price)

        if max_price:
            stmt = stmt.filter(Product.price_product <= max_price)

        if availability:
            stmt = stmt.filter(Product.quantity_product > 0)

        match desc:
            case FilteredDescProduct.NOT_DESC:
                stmt = stmt.order_by(Product.price_product.asc())
            case FilteredDescProduct.DEFAULT:
                pass
            case FilteredDescProduct.DESC:
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
            msg=f"{self.__class__.__name__} Получение всех товаров" " по новым датам"
        )
        stmt = (
            select(Product)
            .options(
                joinedload(Product.product_models_data),
                joinedload(Product.photos),
                joinedload(Product.type_models),
                joinedload(Product.brand_mark),
            )
            .order_by(Product.date_create_product.desc())
        )
        products = (await self.async_session.execute(stmt)).unique().all()

        if products:
            return products
        return None

    async def get_recommended_products(self) -> Union[List, List[Product]]:
        """
        Получение всех рекомендованных товаров
        :session:
        """

        logging.info(msg=f"{self.__class__.__name__} Получение рекомендованных товаров")
        stmt = (
            select(Product)
            .where(Product.is_recommended == True)  # noqa
            .options(
                joinedload(Product.product_models_data),
                joinedload(Product.photos),
                joinedload(Product.type_models),
                joinedload(Product.brand_mark),
            )
        )
        products = (await self.async_session.execute(stmt)).unique().all()
        return products

    async def search(self, id_mark: int | None, id_model: int | None):
        """
        Получение всех товаров по марке - модели
        :param id_mark:
        :param id_model:
        :return:
        """

        stmt = select(Product).options(
            joinedload(Product.photos),
            joinedload(Product.type_models),
            joinedload(Product.brand_mark),
            joinedload(Product.product_models_data),
        )

        if id_model:
            stmt = stmt.filter(
                Product.product_models_data.any(ProductModels.id_model == id_model)
            )

        if id_mark:
            stmt = stmt.filter(Product.brand_mark.any(ProductMarks.id_mark == id_mark))

        result = await self.async_session.execute(stmt)

        return result.unique().all()
