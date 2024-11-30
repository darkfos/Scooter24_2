from src.database.repository.general_repository import GeneralSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.product_photos import ProductPhotos
from typing import Type


class PhotosRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession):
        self.model: Type[ProductPhotos] = ProductPhotos
        super().__init__(session=session, model=self.model)
