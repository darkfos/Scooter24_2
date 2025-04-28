# System
from typing import Type
from abc import ABC, abstractmethod


# Other libraries
from sqlalchemy.ext.asyncio import AsyncSession


# Local
from src.database.repository.user_repository import UserRepository
from src.database.repository.user_type_repository import UserTypeRepository
from src.database.repository.category_repository import CategoryRepository
from src.database.repository.product_repository import ProductRepository
from src.database.repository.vacancies_repository import VacanciesRepository
from src.database.repository.type_worker_repository import TypeWorkerRepository
from src.database.repository.favourite_repository import FavouriteRepository
from src.database.repository.order_repository import OrderRepository
from src.database.repository.review_repository import ReviewRepository
from src.database.repository.subcategory_repository import SubCategoryRepository
from src.database.repository.brand_repository import BrandRepository
from src.database.repository.model_repository import ModelRepository
from src.database.repository.mark_repository import MarkRepository
from src.database.repository.product_models_repository import (
    ProductModelsRepository,
)
from src.database.repository.photos_repository import PhotosRepository
from src.database.repository.type_moto_repository import TypeMotoRepository
from src.database.repository.garage_repository import GarageRepository
from src.database.repository.vacancy_req_repository import (
    VacanciesReqRepository,
)  # noqa
from src.database.repository.product_marks_repository import (
    ProductMarksRepository,
)
from src.database.repository.product_type_models_repository import (
    ProductTypeModelsRepository,
)
from src.database.db_worker import db_work


class IEngineRepository(ABC):

    user_repository: Type[UserRepository]
    user_type_repository: Type[UserTypeRepository]
    category_repository: Type[CategoryRepository]
    product_repository: Type[ProductRepository]
    vacancies_repository: Type[VacanciesRepository]
    type_worker_repository: Type[TypeWorkerRepository]
    favourite_repository: Type[FavouriteRepository]
    order_repository: Type[OrderRepository]
    review_repository: Type[ReviewRepository]
    subcategory_repository: Type[SubCategoryRepository]
    brand_repository: Type[BrandRepository]
    model_repository: Type[ModelRepository]
    mark_repository: Type[MarkRepository]
    product_models_repository: Type[ProductModelsRepository]
    photos_repository: Type[PhotosRepository]
    type_moto_repository: Type[TypeMotoRepository]
    garage_repository: Type[GarageRepository]
    vacancies_req_repository: Type[VacanciesReqRepository]
    product_marks_repository: Type[ProductMarksRepository]
    product_type_models_repository: Type[ProductTypeModelsRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class EngineRepository(IEngineRepository):

    def __init__(self):
        self.session_factory = db_work.async_session
        self.session: AsyncSession

    async def __aenter__(self, *args, **kwargs):
        """
        Получение сессии и её дальнейшее распределение
        по репозиториям
        """

        self.session = self.session_factory()

        self.user_repository: UserRepository = UserRepository(session=self.session)
        self.user_type_repository: UserTypeRepository = UserTypeRepository(
            session=self.session
        )
        self.category_repository: CategoryRepository = CategoryRepository(
            session=self.session
        )
        self.review_repository: ReviewRepository = ReviewRepository(
            session=self.session
        )
        self.order_repository: OrderRepository = OrderRepository(session=self.session)
        self.favourite_repository: FavouriteRepository = FavouriteRepository(
            session=self.session
        )
        self.vacancies_repository: VacanciesRepository = VacanciesRepository(
            session=self.session
        )
        self.product_repository: ProductRepository = ProductRepository(
            session=self.session
        )
        self.type_worker_repository: TypeWorkerRepository = TypeWorkerRepository(
            session=self.session
        )
        self.subcategory_repository: SubCategoryRepository = SubCategoryRepository(
            session=self.session
        )
        self.brand_repository: BrandRepository = BrandRepository(session=self.session)
        self.model_repository: ModelRepository = ModelRepository(session=self.session)
        self.mark_repository: MarkRepository = MarkRepository(session=self.session)
        self.product_models_repository: ProductModelsRepository = (
            ProductModelsRepository(session=self.session)
        )
        self.photos_repository: PhotosRepository = PhotosRepository(
            session=self.session
        )
        self.type_moto_repository: TypeMotoRepository = TypeMotoRepository(
            session=self.session
        )
        self.garage_repository: GarageRepository = GarageRepository(
            session=self.session
        )
        self.vacancies_req_repository: VacanciesReqRepository = VacanciesReqRepository(
            session=self.session
        )
        self.product_marks_repository: ProductMarksRepository = ProductMarksRepository(
            session=self.session
        )
        self.product_type_models_repository: ProductTypeModelsRepository = (
            ProductTypeModelsRepository(session=self.session)
        )

        return self

    async def __aexit__(self, *args):
        """
        Закрытие сессии
        """

        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
