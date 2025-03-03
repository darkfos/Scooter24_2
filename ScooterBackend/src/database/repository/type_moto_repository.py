from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# Local
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.type_moto import TypeMoto


class TypeMotoRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TypeMoto)

    async def find_name(self, name: str):
        stmt = select(TypeMoto).where(TypeMoto.name_moto_type == name)
        result = await self.async_session.execute(stmt)
        return result.one_or_none()
