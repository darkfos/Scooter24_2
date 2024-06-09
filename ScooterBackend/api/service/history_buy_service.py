#System
from typing import List, Union, Dict


#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession


#Local
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.database.models.history_buy import HistoryBuy
from ScooterBackend.database.repository.history_buy_repository import HistoryBuyRepository
from ScooterBackend.api.exception.http_user_exception import UserHttpError
from ScooterBackend.api.exception.http_history_buy_exception import HistoryBuyHttpError
from ScooterBackend.api.dto.history_buy_dto import *
from ScooterBackend.database.repository.admin_repository import AdminRepository


class HistoryBuyService:

    @staticmethod
    async def create_history(
        session: AsyncSession,
        token: str,
        new_history: HistoryBuyBase
    ) -> None:
        """
        Метод сервиса для создания новой истории
        :param session:
        :param token:
        :param new_history:
        :return:
        """

        #Получение данных токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Создание истории
        is_created: bool = await HistoryBuyRepository(session=session).add_one(
            data=HistoryBuy(
                id_user=jwt_data.get("id_user"),
                id_product=new_history.id_product
            )
        )

        if is_created:
            return

        await HistoryBuyHttpError().http_failed_to_create_a_new_history()

    @staticmethod
    async def get_all_histories_for_user(
        session: AsyncSession,
        token: str
    ) -> Union[List, List[HistoryBuyBase]]:
        """
        Метод сервиса для получения всей истории покупок
        :param session:
        :param token:
        :return:
        """

        #Получение данных токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Получение всей истории по id пользователя
        all_user_history: Union[List, List[HistoryBuy]] = await HistoryBuyRepository(session=session).find_by_user_id(
            id_user=jwt_data.get("id_user")
        )

        if all_user_history:
            return [
                HistoryBuyBase(
                    id_product=history.id_product
                )
                for history in all_user_history
            ]
        return all_user_history

    @staticmethod
    async def get_history_by_id(
        session: AsyncSession,
        token: str,
        id_history: int
    ) -> HistoryBuyBase:
        """
        Метод сервиса для получения данных об истории
        :param session:
        :param token:
        :param id_history:
        :return:
        """

        #Получение данных токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Получение всей истории по id пользователя
        history_data: Union[None, HistoryBuy] = await HistoryBuyRepository(session=session).find_one(other_id=id_history)
        if history_data:
            if history_data[0].id_user == jwt_data.get("id_user"):
                return HistoryBuyBase(
                    id_product=history_data[0].id_product
                )
            await UserHttpError().http_user_not_found()
        await HistoryBuyHttpError().http_history_buy_not_found()

    @staticmethod
    async def delete_history_by_id(
        session: AsyncSession,
        token: str,
        id_history: int
    ) -> None:
        """
        Метод сервиса для удаления истории
        :param session:
        :param token:
        :param id_history:
        :return:
        """

        #Получение данных токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_one(other_id=jwt_data.get("id_user"))

        if is_admin:
            is_deleted: bool = await HistoryBuyRepository(session=session).delete_one(other_id=id_history)
            if is_deleted:
                return
            await HistoryBuyHttpError().http_failed_to_delete_history()
        await UserHttpError().http_user_not_found()