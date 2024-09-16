#System
from typing import Union, Type

#Other libraries
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.admin import Admin


class AdminRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Admin] = Admin
        super().__init__(session=session, model=self.model)

    async def find_admin_by_email_and_password(self, email: str, password: str = None) -> Union[Admin, None]:
        """
        Поиск администратора по указанной почте
        :param email:
        :return:
        """

        stmt = select(Admin).where(Admin.email_admin == email if not password else Admin.email_admin == email and Admin.password_user == password)
        res_find_admin: Union[Admin, None] = (await self.async_session.execute(stmt)).one_or_none()

        if res_find_admin:
            return res_find_admin[0]
        return None