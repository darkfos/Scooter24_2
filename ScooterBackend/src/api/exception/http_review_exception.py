from fastapi import HTTPException, status
from src.api.exception.enum_message_for_excp import HeaderMessage
from src.api.exception.global_excp import APIError


class ReviewHttpError(APIError):
    """
    Ошибки связанные с отзывами
    """

    async def http_review_not_found(self):
        """
        Ошибка поиска отзыва
        :return:
        """

        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти отзыв",
        )

    async def http_failed_to_create_a_new_review(self):
        """
        Ошибка создания отзыва
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать отзыв",
        )

    async def http_failed_to_update_review_information(self):
        """
        Ошибка обновления информации об товаре
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить информацию о отзыве",
        )

    async def http_failed_to_delete_review(self):
        """
        Ошибка удаления товара
        :return:
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить отзыв",
        )
