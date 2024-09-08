from fastapi import HTTPException, status
from src.api.exception.enum_message_for_excp import HeaderMessage
from src.api.exception.global_excp import APIError


class HistoryBuyHttpError(APIError):
    """
    Ошибки связанные с историей
    """

    async def http_history_buy_not_found(self):
        """
        Ошибка поиска истории
        :return:
        """

        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти историю о покупках",
        )

    async def http_failed_to_create_a_new_history(self):
        """
        Ошибка создания истории
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать историю покупки",
        )

    async def http_failed_to_update_history_information(self):
        """
        Ошибка обновления информации об истории
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить информацию о истории покупки",
        )

    async def http_failed_to_delete_history(self):
        """
        Ошибка удаления истории
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить историю",
        )