from database.repository.general_repository import GeneralSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, select, Sequence
from database.models.product_photos import ProductPhotos
from typing import Type


class PhotosRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession):
        self.model: Type[ProductPhotos] = ProductPhotos
        super().__init__(session=session, model=self.model)

    async def find_by_product_id(self, id_product: int) -> Sequence[Row]:
        """
        Поиск всех фотографий продукта
        """

        stmt = select(ProductPhotos).where(
            ProductPhotos.id_product == id_product
        )
        res = await self.async_session.execute(stmt)
        all_photos: Sequence[Row] = res.fetchall()
        return all_photos
