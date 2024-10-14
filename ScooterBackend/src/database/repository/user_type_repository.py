from src.database.models.user_type import UserType
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repository.general_repository import GeneralSQLRepository


class UserTypeRepository(GeneralSQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.model = UserType
        super().__init__(session=session, model=self.model)