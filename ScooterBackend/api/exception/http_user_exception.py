from fastapi import HTTPException, status
from ScooterBackend.api.exception.enum_message_for_excp import HeaderMessage
from ScooterBackend.api.exception.global_excp import APIError


class UserHttpError(APIError):
    """
    Ошибки связанные с пользователем
    """

    async def http_user_not_found(self):
        """
        Ошибка поиска пользователя
        :return:
        """

        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти пользователя",
        )

    async def http_failed_to_create_a_new_user(self):
        """
        Ошибка создания пользователя
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать пользователя",
        )

    async def http_failed_to_update_user_information(self):
        """
        Ошибка обновления информации о пользователе
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить пользователя",
        )

    async def http_failed_to_delete_user(self):
        """
        Ошибка удаления пользователя
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить пользователя",
        )