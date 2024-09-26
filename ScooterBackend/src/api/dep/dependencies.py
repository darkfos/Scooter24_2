# System
from typing import Annotated, Type
from abc import ABC, abstractmethod


# Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


# Local
from src.database.repository.user_repository import UserRepository
from src.database.repository.admin_repository import AdminRepository
from src.database.repository.category_repository import CategoryRepository
from src.database.repository.product_repository import ProductRepository
from src.database.repository.vacancies_repository import VacanciesRepository
from src.database.repository.type_worker_repository import TypeWorkerRepository
from src.database.repository.favourite_repository import FavouriteRepository
from src.database.repository.history_buy_repository import HistoryBuyRepository
from src.database.repository.order_repository import OrderRepository
from src.database.repository.review_repository import ReviewRepository
from src.database.db_worker import db_work


class IEngineRepository(ABC):

    user_repository: Type[UserRepository]
    admin_repository: Type[AdminRepository]
    category_repository: Type[CategoryRepository]
    product_repository: Type[ProductRepository]
    vacancies_repository: Type[VacanciesRepository]
    type_worker_repository: Type[TypeWorkerRepository]
    favourite_repository: Type[FavouriteRepository]
    history_buy_repository: Type[HistoryBuyRepository]
    order_repository: Type[OrderRepository]
    review_repository: Type[ReviewRepository]

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass


class EngineRepository(IEngineRepository):

    def __init__(self):
        self.session: AsyncSession

    async def __aenter__(self, *args, **kwargs):
        """
        Получение сессии и её дальнейшее распределение по репозиториям
        """

        self.session = await db_work.get_session()

        self.user_repository = UserRepository(session=self.session)
        self.admin_repository = AdminRepository(session=self.session)
        self.category_repository = CategoryRepository(session=self.session)
        self.review_repository = ReviewRepository(session=self.session)
        self.order_repository = OrderRepository(session=self.session)
        self.favourite_repository = FavouriteRepository(session=self.session)
        self.vacancies_repository = VacanciesRepository(session=self.session)
        self.product_repository = ProductRepository(session=self.session)
        self.type_worker_repository = TypeWorkerRepository(session=self.session)
        self.history_buy_repository = HistoryBuyRepository(session=self.session)

    async def __aexit__(self, *args):
        """
        Закрытие сессии
        """

        await self.session.close()
