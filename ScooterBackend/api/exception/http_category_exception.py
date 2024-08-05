from fastapi import HTTPException, status
from api.exception.enum_message_for_excp import HeaderMessage
from api.exception.global_excp import APIError


class CategoryHttpError(APIError):
    """
    Ошибки связанные с категориями
    """

    async def http_category_not_found(self):
        """
        Ошибка поиска категории
        :return:
        """

        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти категорию",
            header=HeaderMessage.header_find.value
        )

    async def http_failed_to_create_a_new_category(self):
        """
        Ошибка создания категории
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать категорию",
        )

    async def http_failed_to_update_category_information(self):
        """
        Ошибка обновления информации об категории
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить категорию",
            header=HeaderMessage.header_update.value
        )

    async def http_failed_to_delete_category(self):
        """
        Ошибка удаления категории
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить категорию",
        )