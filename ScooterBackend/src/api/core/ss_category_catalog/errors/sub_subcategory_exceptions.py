from src.api.errors.global_excp import APIError
from fastapi import status


class SubSubCategoryException(APIError):

    async def no_create_a_new_sub_subcategory(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать под подкатегорию"
        )

    async def no_found_a_sub_subcategory(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось найти под подкатегорию товара"
        )

    async def no_delete_sub_subcategory(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить под подкатегорию товара"
        )