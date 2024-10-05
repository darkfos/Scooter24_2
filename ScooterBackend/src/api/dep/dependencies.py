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
from src.database.repository.subcategory_repository import SubCategoryRepository
from src.database.repository.sub_sub_categiry_repository import SubSubCategoryRepository
from src.database.repository.brand_repository import BrandRepository
from src.database.repository.model_repository import ModelRepository
from src.database.repository.mark_repository import MarkRepository
from src.database.repository.product_models_repository import ProductModelsRepository
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
    subcategory_repository: Type[SubCategoryRepository]
    sub_subcategory_repository: Type[SubSubCategoryRepository]
    brand_repository: Type[BrandRepository]
    model_repository: Type[ModelRepository]
    mark_repository: Type[MarkRepository]
    product_models_repository: Type[ProductModelsRepository]

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
        try:
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
            self.subcategory_repository = SubCategoryRepository(session=self.session)
            self.sub_subcategory_repository = SubSubCategoryRepository(session=self.session)
            self.brand_repository = BrandRepository(session=self.session)
            self.model_repository = ModelRepository(session=self.session)
            self.mark_repository = MarkRepository(session=self.session)
            self.product_models_repository = ProductModelsRepository(session=self.session)

        except Exception as ex: # Ловим все ошибка ACID (транзакций)
            self.session.rollback()

    async def __aexit__(self, *args):
        """
        Закрытие сессии
        """

        await self.session.close()
