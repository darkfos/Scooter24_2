from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.marks import Mark
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class MarkRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Mark)

    async def find_by_name(self, name_mark):
        stmt = select(Mark).where(Mark.name_mark == name_mark)
        result = await self.async_session.execute(stmt)
        result_data = result.one_or_none()
        if result_data:
            return result_data[0].id
        return result_data
