from fastapi import HTTPException, status
from ScooterBackend.api.exception.enum_message_for_excp import HeaderMessage
from ScooterBackend.api.exception.global_excp import APIError


class FavouriteHttpError(APIError):
    """
    Ошибки связанные с избранными
    """

    async def http_favourite_not_found(self):
        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти избранный товар",
        )

    async def http_failed_to_create_a_new_favourite(self):
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать избранный товар",
        )

    async def http_failed_to_update_favourite_information(self):
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить информацию о избранном товаре",
        )

    async def http_failed_to_delete_favourite(self):
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить избранный товар",
        )