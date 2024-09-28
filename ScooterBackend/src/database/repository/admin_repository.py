# System
from typing import Union, Type
import logging as logger

# Other libraries
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from src.database.repository.general_repository import GeneralSQLRepository
from src.database.models.admin import Admin


logging = logger.getLogger(__name__)


class AdminRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Admin] = Admin
        super().__init__(session=session, model=self.model)

    async def find_admin_by_email_and_password(
        self, email: str, password: str = None
    ) -> Union[Admin, None]:
        """
        Поиск администратора по указанной почте
        :param email:
        :return:
        """

        # Logging
        logging.info(
            msg=f"{self.__class__.__name__} Запрос на получение данных по почте и паролю email={email}; password={password}"
        )

        if email and password:
            stmt = select(Admin).where(Admin.email_admin == email and Admin.password_user == password)
        else:    
            stmt = select(Admin).where(Admin.email_admin == email)
        res_find_admin: Union[Admin, None] = (
            await self.async_session.execute(stmt)
        ).one_or_none()

        if res_find_admin:
            return res_find_admin[0]

        # Logging
        logging.error(
            msg=f"{self.__class__.__name__} не удалось получить данные администратора по почте и паролю email={email}; password={password}"
        )
        return None
