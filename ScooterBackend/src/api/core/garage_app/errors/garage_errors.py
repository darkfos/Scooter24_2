from fastapi import status


# Local
from api.errors.global_excp import APIError


class GarageException(APIError):
    @classmethod
    async def no_create_moto(cls):
        await cls.api_error(
            code=status.HTTP_409_CONFLICT,
            detail_inf="Не удалось добавить транспорт гараж",
        )
