#System
from typing import List, Union, Dict, Coroutine, Any, Type

#Other libraries
...

#Local
from src.api.exception.http_user_exception import UserHttpError
from src.api.exception.http_vacancies_exception import VacanciesHttpError
from src.api.authentication.authentication_service import Authentication
from src.database.repository.vacancies_repository import Vacancies
from src.api.dto.vacancies_dto import VacanciesBase, UpdateVacancies, VacanciesGeneralData
from src.api.dep.dependencies import IEngineRepository

#Redis
from src.store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()


class VacanciesService:

    @staticmethod
    async def create_vacancies(engine: IEngineRepository, token: str, vac_data: VacanciesBase) -> None:
        """
        Метод сервиса для создания новой вакансии
        :session:
        :token:
        :vac_data:
        """

        #Данные токена
        jwt_data: Coroutine[Any, Any, Dict[str, str] | None] = await Authentication().decode_jwt_token(token=token, type_token="access")

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(
                email=jwt_data.get("email")
            )

            if is_admin:
                is_created: bool = await engine.vacancies_repository.add_one(
                    data=Vacancies(
                        salary_employee=vac_data.salary_employee,
                        description_vacancies=vac_data.description_vacancies,
                        id_type_worker=vac_data.id_type_worker
                    )
                )

                if is_created: return
                await VacanciesHttpError().http_dont_create_a_new_vacancies()
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_all_vacancies(engine: IEngineRepository, redis_search_data: str) -> Union[List, List[VacanciesBase]]:
        """
        Метод сервиса для получения списка вакансий
        :session:
        """

        async with engine:
            all_vacancies: Union[List, List[Vacancies]] = await engine.vacancies_repository.find_all()
            if all_vacancies:
                vacancies_data: VacanciesGeneralData = VacanciesGeneralData(
                    vacancies=[
                        {
                            k: v
                            for k, v in vac[0].read_model().items()
                        }
                        for vac in all_vacancies
                    ]
                )
                return vacancies_data
            else:
                return VacanciesGeneralData(vacancies=[{}])

    @redis
    @staticmethod
    async def get_vacancies_by_id(
        engine: IEngineRepository,
        id_vacancies: int,
        redis_search_data: str
    ) -> VacanciesBase:
        """
        Метод сервиса для получения информации о вакансии по id.
        :session:
        :id_vacancies:
        """

        async with engine:
            vacancies_data: Union[None, Vacancies] = await engine.vacancies_repository.find_one(other_id=id_vacancies)

            if vacancies_data:
                return VacanciesBase(
                    salary_employee=vacancies_data[0].salary_employee,
                    description_vacancies=vacancies_data[0].description_vacancies,
                    id_type_worker=vacancies_data[0].id_type_worker
                )
            await VacanciesHttpError().http_vacancies_not_found()

    @staticmethod
    async def update_vacancies(
        engine: IEngineRepository,
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

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(
                email=jwt_data.get("email")
            )

            if is_admin:
                is_updated: bool = await engine.vacancies_repository.update_one(
                    other_id=data_to_update.id,
                    data_to_update=data_to_update
                )
                if is_updated:
                    return
                await VacanciesHttpError().http_dont_update_vacancies()
            await UserHttpError().http_user_not_found()

    @staticmethod
    async def delete_vacancies_by_id(
        engine: IEngineRepository,
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

        async with engine:
            #Проверка на администратора
            is_admin: bool = await engine.admin_repository.find_admin_by_email_and_password(
                email=jwt_data.get("email")
            )

            if is_admin:
                is_deleted: bool = await engine.vacancies_repository.delete_one(other_id=id_vacancies)
                if is_deleted: return
                await VacanciesHttpError().http_dont_delete_vacancies()
            await UserHttpError().http_user_not_found()