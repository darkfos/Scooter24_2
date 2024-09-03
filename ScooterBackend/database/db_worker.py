#Other
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

#System
from typing import Union, ClassVar
#Local

##MODELS##
from database.models.product import Product
from database.models.category import Category
from database.models.order import Order
from database.models.user import User
from database.models.review import Review
from database.models.history_buy import HistoryBuy
from database.models.favourite import Favourite
from database.models.admin import Admin
from database.models.type_worker import TypeWorker
from database.models.vacancies import Vacancies

from settings.database_settings import DatabaseSettings
from database.mainbase import MainBase


class DatabaseEngine:

    __instance: Union[None, ClassVar] = None

    def __new__(cls, *args, **kwargs) -> None:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        return cls.__instance

    def __init__(self):
        self.db_engine = create_async_engine(
            url=DatabaseSettings().db_url,
            echo=True
        )
        self.async_session: async_sessionmaker = async_sessionmaker(bind=self.db_engine)

    async def create_tables(self):
        #Creating tables
        async with self.db_engine.begin() as session:
            await session.run_sync(MainBase.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        #Return session
        async with self.async_session.begin() as session:
            return session

db_work: DatabaseEngine = DatabaseEngine()