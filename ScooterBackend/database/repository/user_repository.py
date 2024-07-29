#System
from typing import Union, List, Type

#Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, Result
from sqlalchemy.orm import joinedload

#Local
from database.models.user import User
from database.repository.general_repository import GeneralSQLRepository


class UserRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: User = User
        super().__init__(session=session, model=self.model)

    async def find_user_by_email_and_password(self, email: str) -> Union[User, bool]:
        """
        Поиск пользователя по почте и паролю
        :param session:
        :param email:
        :param password:
        :return:
        """

        find_user = select(User).where(User.email_user == email)
        result = (await self.async_session.execute(find_user)).one_or_none()
        if result:
            return result[0]
        return False

    async def find_user_and_get_full_information(self, user_id: int) -> Union[User, None]:
        """
        Поиск пользователя и получение полной информации о пользователе
        :param user_id:
        :return:
        """

        stmt = select(User).where(User.id == user_id).options(
            joinedload(User.favourites_user),
            joinedload(User.history_buy_user),
            joinedload(User.orders_user),
            joinedload(User.reviews)
        )
        all_information_about_user = (await self.async_session.execute(stmt)).unique()
        if all_information_about_user:
            return all_information_about_user.scalar()
        return None

    async def find_user_and_get_reviews(self, user_id: int) -> Union[User, None]:
        """
        Получение информации о пользователе, а так же об его отзывах
        :param user_id:
        :return:
        """

        stmt = select(User).where(User.id == user_id).options(
            joinedload(User.reviews)
        )
        user_data = ((await self.async_session.execute(stmt)).unique()).scalar_one_or_none()
        return user_data

    async def find_user_and_get_favourites(self, user_id: int):
        """
        Получение информации по пользователе, а так же об всех его товарах в списке избранное
        :param id_user:
        :return:
        """

        stmt = select(User).where(User.id == user_id).options(
            joinedload(User.favourites_user)
        )
        user_data = ((await self.async_session.execute(stmt)).unique()).scalar_one_or_none()
        return user_data

    async def find_user_and_get_orders(self, user_id: int):
        """
        Получение информаии о пользователе, а так же об всех заказах
        :param user_id:
        :return:
        """

        stmt = select(User).where(User.id == user_id).options(
            joinedload(User.orders_user)
        )
        user_data = ((await self.async_session.execute(stmt)).unique()).scalar_one_or_none()
        return user_data

    async def find_user_and_get_history(self, user_id: int) -> Union[User, None]:
        """
        Получение информации о пользователе, а так же обо всех заказах (история)
        :param user_id:
        :return:
        """

        stmt = select(User).where(User.id == user_id).options(
            joinedload(User.history_buy_user)
        )
        user_data = ((await self.async_session.execute(stmt)).unique()).scalar_one_or_none()
        return user_data

    async def del_more(self, id_users: List[int]) -> bool:
        """
        Удаление нескольких пользователей
        :param args:
        :param kwargs:
        :return:
        """

        for id_user in id_users:
            delete_user: Result = delete(User).where(User.id == id_user)
            await self.async_session.execute(delete_user)
            await self.async_session.commit()

        return True