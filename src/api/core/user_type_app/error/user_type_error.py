from fastapi import status
from src.api.errors.general_exceptions import APIError


class UserTypeException(APIError):
    async def no_create_user_type(self) -> None:
        await self.api_error(
            code=status.HTTP_409_CONFLICT,
            detail_inf="Не удалось создать новую роль",
        )

    async def no_found_user_types(self) -> None:
        await self.api_error(
            code=status.HTTP_404_NOT_FOUND, detail_inf="Не удалось найти роли"
        )
