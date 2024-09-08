#Other
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

#System
from typing import Union
#Local

##MODELS##
from src.database.models.product import Product
from src.database.models.category import Category
from src.database.models.order import Order
from src.database.models.user import User
from src.database.models.review import Review
from src.database.models.history_buy import HistoryBuy
from src.database.models.favourite import Favourite
from src.database.models.admin import Admin
from src.database.models.type_worker import TypeWorker
from src.database.models.vacancies import Vacancies

from src.settings.engine_settings import Settings
from src.database.mainbase import MainBase


class DatabaseEngine:

    __instance: Union[None] = None

    def __new__(cls, *args, **kwargs) -> None:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        return cls.__instance

    def __init__(self):
        self.db_engine = create_async_engine(
            url=Settings.database_settings.db_url,
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