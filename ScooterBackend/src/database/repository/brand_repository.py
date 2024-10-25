from src.database.models.brand import Brand
from src.database.repository.general_repository import GeneralSQLRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BrandRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Brand)

    async def find_by_name(self, name_brand_to_find):
        """
        Поиска бренда по названию
        """

        stmt = select(Brand).where(Brand.name_brand == name_brand_to_find)
        result = await self.async_session.execute(stmt)
        data_result = result.one_or_none()
        if data_result:
            return data_result[0].id
        return data_result
