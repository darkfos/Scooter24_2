from src.api.errors.global_excp import APIError
from fastapi import status


class ModelException(APIError):

    async def no_create_a_new_model(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать новую модель"
        )
    
    async def no_found_a_model_by_id(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось найти модель по идентификатору"
        )

    async def no_delete_model_by_id(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить модель"
        )