# System
from typing import List, Union, Type
import logging as logger

# Local
from api.core.user_app.error.http_user_exception import UserHttpError
from api.core.vacancy_app.error.http_vacancies_exception import (
    VacanciesHttpError,
)
from api.authentication.secure.authentication_service import Authentication
from database.repository.vacancies_repository import Vacancies
from api.core.vacancy_app.schemas.vacancies_dto import (
    VacanciesBase,
    UpdateVacancies,
    VacanciesGeneralData,
    RequestVacancy,
)
from api.dep.dependencies import IEngineRepository
from other.enums.auth_enum import AuthenticationEnum
from database.models.vacancy_request import VacancyRequest

# Redis
from store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class VacanciesService:

    @staticmethod
    async def create_request_on_vacancy(
        engine: IEngineRepository, req_vac: RequestVacancy
    ) -> None:
        """
        Метод сервиса Vacancies - Создание отклика
        :param engine:
        :param req_vac:
        :return:
        """

        async with engine:
            req_vac_is_created = await engine.vacancies_req_repository.add_one(
                data=VacancyRequest(
                    email_user=req_vac.email_user,
                    experience_user=req_vac.experience_user,
                    name_user=req_vac.name_user,
                    telephone_user=req_vac.telephone_user,
                    id_vacancy=req_vac.id_vacancy,
                )
            )

            if req_vac_is_created:
                return

            await VacanciesHttpError().http_dont_create_req_vacancy()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_vacancies(
        engine: IEngineRepository,
        token: str,
        vac_data: VacanciesBase,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для создания новой вакансии
        :session:
        :token:
        :vac_data:
        """

        logging.info(msg=f"{VacanciesService.__name__} Создание новой вакансии")

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                is_created: bool = await engine.vacancies_repository.add_one(
                    data=Vacancies(
                        salary_employee=vac_data.salary_employee,
                        description_vacancies=vac_data.description_vacancies,
                        id_type_worker=vac_data.id_type_worker,
                    )
                )

                if is_created:
                    return
                logging.critical(
                    msg=f"{VacanciesService.__name__} "
                    f"Не удалось создать новую вакансию"
                )
                await VacanciesHttpError().http_dont_create_a_new_vacancies()
            logging.critical(
                msg=f"{VacanciesService.__name__} "
                f"Не удалось создать новую вакансию,"
                f" пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_all_vacancies(
        engine: IEngineRepository, redis_search_data: str
    ) -> Union[List, List[VacanciesBase]]:
        """
        Метод сервиса для получения списка вакансий
        :session:
        """

        logging.info(
            msg=f"{VacanciesService.__name__} " f"Получение списка вакансий"
        )
        async with engine:
            all_vacancies: Union[List, List[Vacancies]] = (
                await engine.vacancies_repository.find_all_with_tp_worker()
            )
            if all_vacancies:
                vacancies_data: VacanciesGeneralData = VacanciesGeneralData(
                    vacancies=[
                        VacanciesBase(
                            salary_employee=vac.salary_employee,
                            description_vacancies=vac.description_vacancies,
                            is_worked=vac.is_worked,
                            type_work=vac.type_work.read_model(),
                            id_vacancy=vac.id,
                        )
                        for vac in all_vacancies
                    ]
                )
                return vacancies_data
            else:
                return VacanciesGeneralData(vacancies=[{}])

    @redis
    @staticmethod
    async def get_vacancies_by_id(
        engine: IEngineRepository, id_vacancies: int, redis_search_data: str
    ) -> VacanciesBase:
        """
        Метод сервиса для получения информации о вакансии по id.
        :session:
        :id_vacancies:
        """

        logging.info(
            msg=f"{VacanciesService.__name__} "
            f"Получение информации о вакансии по "
            f"id={id_vacancies}"
        )
        async with engine:
            vacancies_data: Union[None, Vacancies] = (
                await engine.vacancies_repository.find_one(
                    other_id=id_vacancies
                )
            )

            if vacancies_data:
                return VacanciesBase(
                    salary_employee=vacancies_data[0].salary_employee,
                    description_vacancies=vacancies_data[
                        0
                    ].description_vacancies,
                    id_type_worker=vacancies_data[0].id_type_worker,
                )
            logging.critical(
                msg=f"{VacanciesService.__name__} "
                f"Не удалось получить информацию о заказе,"
                f" заказ не был найден"
            )
            await VacanciesHttpError().http_vacancies_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_vacancies(
        engine: IEngineRepository,
        token: str,  # noqa
        data_to_update: UpdateVacancies,
        token_data: dict = dict(),
    ):
        """
        Метод сервиса для обновления вакансии
        :session:
        :token:
        :data_to_update:
        """

        logging.info(msg=f"{VacanciesService.__name__} Обновление вакансии")

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                is_updated: bool = await engine.vacancies_repository.update_one(
                    other_id=data_to_update.id, data_to_update=data_to_update
                )
                if is_updated:
                    return
                logging.critical(
                    msg=f"{VacanciesService.__name__} "
                    f"Не удалось обновить вакансию"
                )
                await VacanciesHttpError().http_dont_update_vacancies()
            logging.critical(
                msg=f"{VacanciesService.__name__} "
                f"Не удалось обновить вакансию,"
                f" пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_vacancies_by_id(
        engine: IEngineRepository,
        token: str,
        id_vacancies: int,
        token_data: dict = dict(),
    ):
        """
        Метод сервиса для удаления вакансии
        :session:
        :token:
        :id_vacancies:
        """

        logging.info(msg=f"{VacanciesService.__name__} Удаление вакансии")

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                is_deleted: bool = await engine.vacancies_repository.delete_one(
                    other_id=id_vacancies
                )
                if is_deleted:
                    return
                logging.critical(
                    msg=f"{VacanciesService.__name__} Не удалось"
                    f" удалить вакансию"
                )
                await VacanciesHttpError().http_dont_delete_vacancies()
            logging.critical(
                msg=f"{VacanciesService.__name__} "
                f"Не удалось удалить вакансию,"
                f" пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()
