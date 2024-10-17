# System
from typing import List, Union
import logging as logger

# Local
from src.api.authentication.secure.authentication_service import Authentication
from src.database.models.history_buy import HistoryBuy
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.core.history_catalog.error.http_history_buy_exception import (
    HistoryBuyHttpError,
)
from src.api.core.history_catalog.schemas.history_buy_dto import HistoryBuyBase
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum


auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class HistoryBuyService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_history(
        engine: IEngineRepository,
        token: str,
        new_history: HistoryBuyBase,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для создания новой истории
        :param session:
        :param token:
        :param new_history:
        :return:
        """

        logging.info(msg=f"{HistoryBuyService.__name__} Создание новой истории")

        async with engine:
            # Создание истории
            is_created: bool = await engine.history_buy_repository.add_one(
                data=HistoryBuy(
                    id_user=token_data.get("id_user"),
                    id_product=new_history.id_product,
                )
            )

            if is_created:
                return
            logging.critical(
                msg=f"{HistoryBuyService.__name__} Не удалось"
                f" создать новую историю"
            )
            await HistoryBuyHttpError().http_failed_to_create_a_new_history()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_all_histories_for_user(
        engine: IEngineRepository, token: str, token_data: dict = dict()
    ) -> Union[List, List[HistoryBuyBase]]:
        """
        Метод сервиса для получения всей истории покупок
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{HistoryBuyService.__name__} Получение всей истории покупок"
        )

        async with engine:
            # Получение всей истории по id пользователя
            all_user_history: Union[List, List[HistoryBuy]] = (
                await engine.history_buy_repository.find_by_user_id(
                    id_user=token_data.get("id_user")
                )
            )

            if all_user_history:
                return [
                    HistoryBuyBase(id_product=history.id_product)
                    for history in all_user_history
                ]
            return all_user_history

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_history_by_id(
        engine: IEngineRepository,
        token: str,
        id_history: int,
        token_data: dict = dict(),
    ) -> HistoryBuyBase:
        """
        Метод сервиса для получения данных об истории
        :param session:
        :param token:
        :param id_history:
        :return:
        """

        logging.info(
            msg=f"{HistoryBuyService.__name__} Получение данных об истории"
        )

        async with engine:
            # Получение всей истории по id пользователя
            history_data: Union[None, HistoryBuy] = (
                await engine.history_buy_repository.find_one(
                    other_id=id_history
                )
            )
            if history_data:
                if history_data[0].id_user == token_data.get("id_user"):
                    return HistoryBuyBase(id_product=history_data[0].id_product)
                logging.critical(
                    msg=f"{HistoryBuyService.__name__} Не удалось"
                    f" получить данные"
                    f" об истории, пользователь"
                    f" не был найден"
                )
                await UserHttpError().http_user_not_found()
            logging.critical(
                msg=f"{HistoryBuyService.__name__} Не удалось получить данные"
                f" об истории, не была найдена история"
            )
            await HistoryBuyHttpError().http_history_buy_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_history_by_id(
        engine: IEngineRepository,
        token: str,
        id_history: int,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для удаления истории
        :param session:
        :param token:
        :param id_history:
        :return:
        """

        logging.info(
            msg=f"{HistoryBuyService.__name__} Удаление истории "
            f"id_history={id_history}"
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = await engine.history_buy_repository.find_one(
                other_id=token_data.get("id_user")
            )

            if is_admin:
                is_deleted: bool = (
                    await engine.history_buy_repository.delete_one(
                        other_id=id_history
                    )
                )
                if is_deleted:
                    return
                await HistoryBuyHttpError().http_failed_to_delete_history()
            logging.critical(
                msg=f"{HistoryBuyService.__name__} Не удалось удалить историю,"
                f" id_history={id_history}"
            )
            await UserHttpError().http_user_not_found()
