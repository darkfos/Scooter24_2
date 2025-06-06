from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from typing import Union

from src.database.models.product import Product  # noqa
from src.database.models.category import Category  # noqa
from src.database.models.order import Order  # noqa
from src.database.models.user import User  # noqa
from src.database.models.review import Review  # noqa
from src.database.models.favourite import Favourite  # noqa
from src.database.models.type_worker import TypeWorker  # noqa
from src.database.models.vacancies import Vacancies  # noqa
from src.database.models.subcategory import SubCategory  # noqa
from src.database.models.product_models import ProductModels  # noqa
from src.database.models.user_type import UserType  # noqa
from src.database.models.vacancy_request import VacancyRequest  # noqa
from src.database.models.order_products import OrderProducts  # noqa
from src.settings.database_settings.database_settings import (
    DatabaseSettings,
)  # noqa

from src.database.mainbase import MainBase


class DatabaseEngine:

    __instance: Union[None, "DatabaseEngine"] = None

    def __new__(cls, *args, **kwargs) -> "DatabaseEngine":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.db_engine: AsyncEngine = create_async_engine(
            url=DatabaseSettings().db_url, echo=True
        )
        self.async_session: async_sessionmaker = async_sessionmaker(
            bind=self.db_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def create_tables(self):
        async with self.db_engine.begin() as session:
            await session.run_sync(MainBase.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        async with self.async_session.begin() as session:
            return session


db_work: DatabaseEngine = DatabaseEngine()
