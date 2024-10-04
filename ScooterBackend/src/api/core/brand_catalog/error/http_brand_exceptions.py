from src.api.errors.global_excp import APIError
from fastapi import status


class BrandException(APIError):

    async def no_create_a_new_brand(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать новый бренд"
        )

    async def no_found_a_brand(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось найти бренд по указанному идентификатору"
        )

    async def no_delete_a_brand(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить бренд"
        )