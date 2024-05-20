#Other
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

#Local
from ScooterBackend.settings import DatabaseSettings


class DatabaseEngine:

    def __init__(self):
        self.db_engine = create_async_engine(
            url=DatabaseSettings().db_url,
            echo=True
        )
        self.async_session: async_sessionmaker = async_sessionmaker(bind=self.db_engine)

    async def create_tables(self, MainBase):
        #Creating tables
        async with self.db_engine.begin() as session:
            await session.run_sync(MainBase.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        #Return session
        async with self.async_session() as session:
            yield session

db_work: DatabaseEngine = DatabaseEngine()