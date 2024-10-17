from src.api.errors.global_excp import APIError
from fastapi import status
from typing import NoReturn


class MarkException(APIError):

    async def not_found_a_mark(self) -> NoReturn:
        await self.api_error(
            code=status.HTTP_404_NOT_FOUND, detail_inf="Не удалось найти марку"
        )

    async def no_create_a_new_mark(self) -> NoReturn:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать марку",
        )

    async def no_delete_mark(self) -> NoReturn:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить марку",
        )
