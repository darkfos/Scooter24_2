from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.order_products import OrderProducts


class OrderProductsRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=OrderProducts)
