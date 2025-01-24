# Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from typing import Type
import logging as logger

# Local
...


logging = logger.getLogger(__name__)


class GeneralSQLRepository:

    def __init__(self, session: AsyncSession, model=None):
        self.model = model
        self.async_session: Type[AsyncSession] = session

    async def add_one(self, data: dict) -> bool:
        """
        Добавление 1 записи
        :param data:
        :return:
        """

        try:
            logging.info(
                msg=f"{self.model.__class__.__name__} "
                f"Добавление записи, data={data}"
            )
            stmt = (
                insert(self.model)
                .values(data.read_model())
                .returning(self.model.id)
            )
            result = await self.async_session.execute(stmt)
            if result:
                await self.async_session.commit()
                return result.scalar()
            else:
                logging.exception(
                    msg=f"{self.model.__class__.__name__} "
                    f"Не удалось добавить новую запись"
                )
                raise Exception
        except Exception:
            await self.async_session.rollback()
            return False

    async def find_one(self, other_id: int):
        """
        Поиск 1 записи по ключу
        :param other_id:
        :return:
        """

        logging.info(
            msg=f"{self.model.__class__.__name__} "
            f"Получение записи по "
            f"ключу = {other_id}"
        )
        stmt = select(self.model).where(self.model.id == other_id)
        information_about_object = await self.async_session.execute(stmt)
        return information_about_object.fetchone()

    async def find_all(self):
        """
        Получение всех записей
        :return:
        """

        logging.info(
            msg=f"{self.model.__class__.__name__} " f"Получение всех записей"
        )
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

        print(data_to_update)

        logging.info(
            msg=f"{self.model.__class__.__name__} "
            f"Обновление данных по "
            f"id={other_id},"
            f" data={data_to_update}"
        )

        stmt = (
            update(self.model)
            .where(self.model.id == other_id)
            .values(data_to_update)
        )

        try:
            update_data = await self.async_session.execute(stmt)
            if update_data:
                await self.async_session.commit()
                return True
            else:
                logging.exception(
                    msg=f"{self.model.__class__.__name__} "
                    f"Не удалось обновить данные"
                )
                raise Exception
        except Exception as ex:
            print(ex)
            await self.async_session.rollback()
            return False

    async def delete_one(self, other_id: int) -> bool:
        """
        Удаление 1 записи
        :param other_id:
        :return:
        """

        logging.info(
            msg=f"{self.model.__class__.__name__} "
            f"Удаление записи по "
            f"id={other_id}"
        )
        stmt = delete(self.model).where(self.model.id == other_id)
        res_to_del: int = (await self.async_session.execute(stmt)).rowcount
        if res_to_del:
            await self.async_session.commit()
            if res_to_del > 0:
                return True
        else:
            await self.async_session.rollback()
            logging.critical(
                msg=f"{self.model.__class__.__name__} "
                f"Не удалось удалить запись по "
                f"id={other_id}"
            )
            return False
