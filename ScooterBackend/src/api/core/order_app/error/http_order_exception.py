from fastapi import status
from api.errors.global_excp import APIError


class OrderHttpError(APIError):
    """
    Ошибки связанные с заказами
    """

    async def http_order_not_found(self):
        """
        Ошибка поиска заказа
        :return:
        """
        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти заказ",
        )

    async def http_failed_to_create_a_new_order(self):
        """
        Ошибка создания заказа
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать заказ",
        )

    async def http_failed_to_update_order_information(self):
        """
        Ошибка обновления информации об заказе
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить информацию о заказе",
        )

    async def http_failed_to_delete_order(self):
        """
        Ошибка удаления заказа
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить заказ",
        )
