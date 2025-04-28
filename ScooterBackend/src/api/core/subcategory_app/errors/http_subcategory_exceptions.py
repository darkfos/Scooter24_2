from src.api.errors.global_excp import APIError
from fastapi import status


class SubCategoryException(APIError):

    async def no_create_a_new_subcategory(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать новую подкатегорию",
        )

    async def no_found_a_subcategory(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось найти подкатегорию по "
            "указанному идентификатору",
        )

    async def no_delete_a_subcategory(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить подкатегорию",
        )
