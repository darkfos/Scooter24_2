from api.errors.global_excp import APIError
from fastapi import status


class PhotoAPIError(APIError):

    async def photo_not_found(self) -> None:
        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Фотография не была найдена",
        )

    async def photos_not_found(self) -> None:
        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Фотографии не были найдены",
        )
