from sqlalchemy.ext.asyncio import AsyncSession


# Local
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.type_moto import TypeMoto


class TypeMotoRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TypeMoto)
