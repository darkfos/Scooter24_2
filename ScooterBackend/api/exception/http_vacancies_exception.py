#Other libraries
from fastapi import status

#Local
from ScooterBackend.api.exception.global_excp import APIError


class VacanciesHttpError(APIError):

    async def http_dont_create_a_new_vacancies(self):
        """
        Ошибка создание новой вакансии
        """

        return await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось создать вакансию"
        )

    async def http_vacancies_not_found(self):
        """
        Ошибка поиска вакансии
        """

        return await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось найти вакансию"
        )

    async def http_dont_delete_vacancies(self):
        """
        Ошибка удаления вакансии
        """

        return await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось удалить вакансию"
        )

    async def http_dont_update_vacancies(self):
        """
        Ошибка обновления информации о вакансии
        """

        return await self.api_error(
            code=status.HTTP_400_BAD_REQUEST,
            detail_inf="Не удалось обновить информацию"
        )