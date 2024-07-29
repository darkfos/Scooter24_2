#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert

#Local
from database.models.product import Product


class GeneralSQLRepository:

    def __init__(self, session: AsyncSession, model=None):
        self.model = model
        self.async_session = session

    async def add_one(self, data: dict) -> bool:
        """
        Добавление 1 записи
        :param data:
        :return:
        """

        try:
            stmt = insert(self.model).values(data.read_model()).returning(self.model.id)
            result = await self.async_session.execute(stmt)
            await self.async_session.commit()
            return result.scalar()
        except Exception as ex:
            return False

    async def find_one(self, other_id: int):
        """
        Поиск 1 записи по ключу
        :param other_id:
        :return:
        """

        stmt = select(self.model).where(self.model.id == other_id)
        information_about_object = await self.async_session.execute(stmt)
        return information_about_object.fetchone()

    async def find_all(self):
        """
        Получение всех записей
        :return:
        """

        stmt = select(self.model)
        all_info = await self.async_session.execute(stmt)
        return all_info.fetchall()

    async def update_one(self, other_id: int, data_to_update: dict) -> None:
        """
        Обновление данных 1 записи
        :param other_id:
        :param data_to_update:
        :return:
        """

        data_to_update = {data: data_to_update.get(data) for data in data_to_update if data_to_update.get(data) != None}
        stmt = update(self.model).where(self.model.id == other_id).values(data_to_update)
        try:
            await self.async_session.execute(stmt)
            await self.async_session.commit()
            return True
        except Exception as ex:
            return False

    async def delete_one(self, other_id: int) -> bool:
        """
        Удаление 1 записи
        :param other_id:
        :return:
        """

        stmt = delete(self.model).where(self.model.id == other_id)
        res_to_del: int = (await self.async_session.execute(stmt)).rowcount
        await self.async_session.commit()
        if res_to_del > 0: return True
        return False