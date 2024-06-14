#System
from typing import List, Union, Dict

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.api.exception.http_user_exception import UserHttpError
from ScooterBackend.api.exception.http_vacancies_exception import VacanciesHttpError
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.database.repository.admin_repository import AdminRepository
from ScooterBackend.database.repository.vacancies_repository import VacanciesRepository, Vacancies
from ScooterBackend.api.dto.vacancies_dto import VacanciesBase, UpdateVacancies


class VacanciesService:

    @staticmethod
    async def create_vacancies(session: AsyncSession, token: str, vac_data: VacanciesBase) -> None:
        """
        Метод сервиса для создания новой вакансии
        :session:
        :token:
        :vac_data:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(
            email=jwt_data.get("email")
        )

        if is_admin:
            is_created: bool = await VacanciesRepository(session=session).add_one(
                data=Vacancies(
                    salary_employee=vac_data.salary_employee,
                    description_vacancies=vac_data.description_vacancies,
                    id_type_worker=vac_data.id_type_worker
                )
            )

            if is_created: return
            await VacanciesHttpError().http_dont_create_a_new_vacancies()
        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_all_vacancies(session: AsyncSession) -> Union[List, List[VacanciesBase]]:
        """
        Метод сервиса для получения списка вакансий
        :session:
        """

        all_vacancies: Union[List, List[Vacancies]] = await VacanciesRepository(session=session).find_all()

        if all_vacancies:
            return [
                VacanciesBase(
                    salary_employee=vac[0].salary_employee,
                    description_vacancies=vac[0].description_vacancies,
                    id_type_worker=vac[0].id_type_worker
                )
                for vac in all_vacancies
            ]
        else:
            return []

    @staticmethod
    async def get_vacancies_by_id(
        session: AsyncSession,
        id_vacancies: int
    ) -> VacanciesBase:
        """
        Метод сервиса для получения информации о вакансии по id.
        :session:
        :id_vacancies:
        """

    @staticmethod
    async def update_vacancies(
        session: AsyncSession,
        token: str,
        data_to_update: UpdateVacancies
    ):
        """
        Метод сервиса для обновления вакансии
        :session:
        :token:
        :data_to_update:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(
            email=jwt_data.get("email")
        )

        if is_admin:
            is_updated: bool = VacanciesRepository(session=session).update_one(
                other_id=data_to_update.id,
                data_to_update=data_to_update
            )
            if is_updated:
                return
            await VacanciesHttpError().http_dont_update_vacancies()
        await UserHttpError().http_user_not_found()

    @staticmethod
    async def delete_vacancies_by_id(
        session: AsyncSession,
        token: str,
        id_vacancies: int,
    ):
        """
        Метод сервиса для удаления вакансии
        :session:
        :token:
        :id_vacancies:
        """

        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(
            email=jwt_data.get("email")
        )

        if is_admin:
            is_deleted: bool = await VacanciesRepository(session=session).delete_one(other_id=id_vacancies)
            if is_deleted: return
            await VacanciesHttpError().http_dont_delete_vacancies()
        await UserHttpError().http_user_not_found()