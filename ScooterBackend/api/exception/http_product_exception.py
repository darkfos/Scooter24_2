from fastapi import HTTPException, status
from ScooterBackend.api.exception.enum_message_for_excp import HeaderMessage
from ScooterBackend.api.exception.global_excp import APIError


class ProductHttpError(APIError):
    """
    Ошибки связанные с товарами
    """

    async def http_product_not_found(self):
        """
        Ошибка поиска товара
        :return:
        """
        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти товар",
        )

    async def http_failed_to_create_a_new_product(self):
        """
        Ошибка создания заказа
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать товар",
        )

    async def http_failed_to_update_product_information(self):
        """
        Ошибка обновления информации об товаре
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить информацию о товаре",
        )

    async def http_failed_to_delete_product(self):
        """
        Ошибка удаления товара
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить товар",
        )