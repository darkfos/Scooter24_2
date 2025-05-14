# System
from typing import Union, List, Type
import logging as logger

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, Result
from sqlalchemy.orm import joinedload

from src.database.models.order_products import OrderProducts
from src.database.models.product import Product

# Local
from src.database.models.user import User
from src.database.models.order import Order
from src.database.repository.general_repository import GeneralSQLRepository
from src.other.enums.user_type_enum import UserTypeEnum
from src.database.models.enums.order_enum import OrderTypeOperationsEnum


logging = logger.getLogger(__name__)


class UserRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[User] = User
        super().__init__(session=session, model=self.model)

    async def find_user_by_email_and_password(
        self, email: str
    ) -> Union[User, bool]:
        """
        Поиск пользователя по почте
        :param session:
        :param email:
        :param password:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} Поиск пользователя по "
            f"почте={email}"
        )
        find_user = select(User).where(User.email_user == email)
        result = (await self.async_session.execute(find_user)).one_or_none()
        if result:
            return result[0]
        logging.critical(
            msg=f"{self.__class__.__name__}"
            f" Не был найден пользователь"
            f" по почте={email}"
        )
        return False

    async def find_user_and_get_full_information(
        self, user_id: int
    ) -> Union[User, None]:
        """
        Поиск пользователя и получение полной информации о пользователе
        :param user_id:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__}"
            f" Поиск пользователя и получение полной"
            f" информации о пользователе id_user={user_id}"
        )
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                joinedload(User.favourites_user),
                joinedload(User.orders_user),
                joinedload(User.reviews),
            )
        )
        all_information_about_user = (
            await self.async_session.execute(stmt)
        ).unique()
        if all_information_about_user:
            return all_information_about_user.scalar()
        logging.critical(
            msg=f"{self.__class__.__name__} Не удалось найти"
            f" пользователя по id_user={user_id}"
        )
        return None

    async def find_user_and_get_reviews(
        self, user_id: int
    ) -> Union[User, None]:
        """
        Получение информации о пользователе, а так же об его отзывах
        :param user_id:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Получение информации о пользователе"
            f" и о всех его отзывах id_user={user_id}"
        )
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.reviews))
        )
        user_data = (
            (await self.async_session.execute(stmt)).unique()
        ).scalar_one_or_none()
        return user_data

    async def find_user_and_get_favourites(self, user_id: int):
        """
        Получение информации по пользователе, а так
        же об всех его товарах в списке избранное
        :param id_user:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Получение информации о пользователе"
            f" и о всех его товарах в списке избранное"
            f" id_user={user_id}"
        )
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.favourites_user))
        )
        user_data = (
            (await self.async_session.execute(stmt)).unique()
        ).scalar_one_or_none()
        return user_data

    async def find_user_and_get_orders(self, user_id: int):
        """
        Получение информаии о пользователе, а так же об всех заказах
        :param user_id:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Получение информации о "
            f"пользователе и о всех его заказах"
            f" id_user={user_id}"
        )
        stmt = (
            select(Order)
            .where(Order.id_user == user_id)
            .options(
                joinedload(Order.product_list),
                joinedload(Order.product_list).joinedload(OrderProducts.product_data),
                joinedload(Order.product_list).joinedload(OrderProducts.product_data).joinedload(Product.photos),
            )
            .where(
                Order.type_operation.in_(
                    [
                        OrderTypeOperationsEnum.NO_BUY.value,
                    ]
                )
            )
        )
        user_data = ((await self.async_session.execute(stmt)).unique()).all()
        return user_data

    async def success_user_orders(self, user_id: int):
        """
        Получение всех оплаченных пользователем заказов
        :param user_id:
        :return:
        """

        stmt = (
            select(Order)
            .options(joinedload(Order.product_list).joinedload(
                OrderProducts.product_data
            ))
            .where(
                Order.id_user == user_id
                and (  # noqa
                    Order.type_operation.in_(
                        OrderTypeOperationsEnum.SUCCESS,
                        OrderTypeOperationsEnum.RETURNED,
                        OrderTypeOperationsEnum.DELIVERED
                    )
                )
            )
        )

        result = await self.async_session.execute(stmt)

        return result.unique().all()

    async def find_user_and_get_history(
        self, user_id: int
    ) -> Union[User, None]:
        """
        Получение информации о пользователе, а так
        же обо всех заказах (история)
        :param user_id:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Получение информации"
            f" о пользователе и о всей"
            f" истории id_user={user_id}"
        )

        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.history_buy_user))
        )
        user_data = (
            (await self.async_session.execute(stmt)).unique()
        ).scalar_one_or_none()
        return user_data

    async def del_more(self, id_users: List[int]) -> bool:
        """
        Удаление нескольких пользователей
        :param args:
        :param kwargs:
        :return:
        """

        logging.info(
            msg=f"{self.__class__.__name__} "
            f"Удаление пользователей id_users={id_users}"
        )
        for id_user in id_users:
            delete_user: Result = delete(User).where(User.id == id_user)
            await self.async_session.execute(delete_user)
            await self.async_session.commit()

        return True

    async def find_admin(self, id_: str) -> bool:
        """
        Проверка на администратора
        :param email:
        :return:
        """

        try:
            stmt = select(User).where(
                User.id == id_, User.id_type_user == UserTypeEnum.ADMIN.value
            )
            result = (await self.async_session.execute(stmt)).fetchone()
            return True if result else False
        except Exception:
            return False
