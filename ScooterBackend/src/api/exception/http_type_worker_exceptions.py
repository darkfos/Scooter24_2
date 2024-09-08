#Other libraries
from fastapi import status

#Local
from src.api.exception.global_excp import APIError


class TypeWorkerExceptions(APIError):

    async def http_dont_create_a_new_type_worker(self):
        """
        Ошибка с созданием нового типа работника
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать нового типа работника"
        )

    async def http_not_found_type_worker(self):
        """
        Ошибка с поиском типа работника
        """

        await self.api_error(
            code=status.HTTP_404_NOT_FOUND,
            detail_inf="Не удалось найти работника"
        )

    async def http_dont_delete_type_worker(self):
        """
        Ошибка удаления типа работника
        """

        await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить тип работника"
        )