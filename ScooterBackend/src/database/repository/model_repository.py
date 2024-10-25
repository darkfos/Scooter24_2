from src.database.repository.general_repository import GeneralSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models.model import Model


class ModelRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Model)

    async def find_by_name(self, name_model):
        stmt = select(Model).where(Model.name_model == name_model)
        result = await self.async_session.execute(stmt)
        data_result = result.one_or_none()
        if data_result:
            return data_result[0].id
        return data_result
