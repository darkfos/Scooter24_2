from src.database.models.product_type_models import ProductTypeModels
from src.database.repository.general_repository import GeneralSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ProductTypeModelsRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession, model=ProductTypeModels) -> None:
        super().__init__(session=session, model=model)
