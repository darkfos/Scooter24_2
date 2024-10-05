from src.api.errors.global_excp import APIError
from fastapi import status


class ProductModelsException(APIError):

    async def no_create_a_new_product_models(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось добавить новую модель для товара"
        )

    async def no_found_a_product_models_by_id_product(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось найти модели для товара" 
        )

    async def no_to_delete_product_models_by_id(self) -> None:
        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить запись из моделей продуктов по идентификатору"
        )