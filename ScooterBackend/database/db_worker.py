#Other
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

#Local

##MODELS##
from ScooterBackend.database.models.product import Product
from ScooterBackend.database.models.category import Category
from ScooterBackend.database.models.order import Order
from ScooterBackend.database.models.user import User
from ScooterBackend.database.models.review import Review
from ScooterBackend.database.models.history_buy import HistoryBuy
from ScooterBackend.database.models.favourite import Favourite
from ScooterBackend.database.models.admin import Admin
from ScooterBackend.database.models.type_worker import TypeWorker
from ScooterBackend.database.models.vacancies import Vacancies

from ScooterBackend.settings.database_settings import DatabaseSettings
from ScooterBackend.database.mainbase import MainBase


class DatabaseEngine:

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