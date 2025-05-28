from src.api.errors.global_excp import APIError
from src.api.errors.enum_message_for_excp import HeaderMessage
from fastapi import status


class GeneralExceptions(APIError):

    async def http_auth_error(self):
        await self.api_error(
            code=status.HTTP_401_UNAUTHORIZED,
            detail_inf="Не верный токен",
        )

    async def http_time_error(self):
        await self.api_error(
            code=status.HTTP_408_REQUEST_TIMEOUT,
            detail_inf="Превышено время работы запроса",
            header=HeaderMessage.header_auth.value,
        )

    async def http_data_error(self):
        await self.api_error(
            code=status.HTTP_409_CONFLICT,
            detail_inf="Не удалось обработать файлы",
        )

    async def http_not_allowed_method(self):
        await self.api_error(
            code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail_inf="Запрещенный метод",
            header=HeaderMessage.header_find.value,
        )
