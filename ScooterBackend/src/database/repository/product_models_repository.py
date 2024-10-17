from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.product_models import ProductModels
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class ProductModelsRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=ProductModels)

    async def find_all_models_by_id_product(
        self, id_product: int
    ) -> List[ProductModels]:
        stmt = select(self.model).where(self.model.id_product == id_product)
        result = (await self.async_session.execute(stmt)).fetchall()
        return result
