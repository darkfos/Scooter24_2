from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.repository.product_repository import ProductRepository
from src.database.repository.category_repository import CategoryRepository
from src.database.models.product_category import ProductCategory
from typing import Type
import logging


class ProductCategoryRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession, model=ProductCategory):
        super().__init__(session, model)
        self.category_rep: Type[CategoryRepository] = CategoryRepository(
            session=session
        )
        self.product_rep: Type[ProductRepository] = ProductRepository(session=session)

    async def add_new_category(self, id_product: int, id_category: int) -> bool:
        """
        Добавление новой категории в товар
        """

        logging.info(msg=f"{self.__class__.__name__} Добавление новой категории в товар id_product = {id_product}, id_category = {id_category}")
        is_created_category = await self.category_rep.find_one(other_id=id_category)
        is_created_product = await self.product_rep.find_one(other_id=id_product)

        if is_created_category and is_created_product:

            # Add new category
            is_created = await self.add_one(
                data=ProductCategory(id_category=id_category, id_product=id_product)
            )
            return True if is_created else False
        
        logging.critical(msg=f"{self.__class__.__name__} Не удалось добавить новую категорию к товару")
        return False
