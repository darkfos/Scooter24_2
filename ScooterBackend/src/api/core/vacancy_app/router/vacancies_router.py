# System
from typing import Annotated, Type
import logging

# Other libraries
from fastapi import status, Depends, APIRouter

# Local
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.vacancy_app.schemas.vacancies_dto import (
    VacanciesBase,
    UpdateVacancies,
    VacanciesGeneralData,
    RequestVacancy,
)
from src.api.core.vacancy_app.service.vacancies_service import (
    VacanciesService,
)
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix


auth: Authentication = Authentication()
vacancies_router: APIRouter = APIRouter(
    prefix=APIPrefix.VACANCIES_PREFIX.value, tags=[APITagsEnum.VACANCIES.value]
)
logger: Type[logging.Logger] = logging.getLogger(__name__)


@vacancies_router.post(
    path="/create",
    description="""
    ### Endpoint - создание новой вакансии.
    Данный метод позволяет создать новую вакансию.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Создание вакансии",
    response_model=None,
    status_code=status.HTTP_200_OK,
    tags=["AdminPanel - Панель администратора"],
)
async def create_a_new_vacancies(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    new_vacancies: VacanciesBase,
) -> None:
    """
    ENDPOINT - Создание новой вакансии
    :session:
    :admin_data:
    :new_vacancies:
    """

    logger.info(
        msg="Vacancy-Router вызов метода создания"
        " новой вакансии (create_a_new_vacancies)"
    )

    return await VacanciesService.create_vacancies(
        engine=session, token=admin_data, vac_data=new_vacancies
    )


@vacancies_router.post(
    path="/create/req",
    description="""
    ### ENDPOINT - Создание отклика на вакансию
    Доступен любому пользователю
    """,
    summary="Создание отклика",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def create_req_vacancy(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    vacancy_data: RequestVacancy,
) -> None:
    """
    Создание отклика на вакансию
    :param engine:
    :param vacancy_data:
    :return:
    """

    return await VacanciesService.create_request_on_vacancy(
        engine=engine, req_vac=vacancy_data
    )


@vacancies_router.get(
    path="/all",
    description="""
    ### Endpoint - Получение всех вакансий.
    Данный метод позволяет получить все вакансии.
    """,
    summary="Список всех вакансий",
    response_model=VacanciesGeneralData,
    status_code=status.HTTP_200_OK,
)
async def get_all_vacancies(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> VacanciesGeneralData:
    """
    ENDPOINT - Получение все вакансий.
    """

    logger.info(
        msg="Vacancy-Router вызов метода получения" " всех вакансий (get_all_vacancies)"
    )

    return await VacanciesService.get_all_vacancies(
        engine=session, redis_search_data="all_vacancies"
    )


@vacancies_router.get(
    path="/vacancy/{id_vacancies}",
    description="""
    ### Endpoint - Получение вакансии по id.
    Данный метод позволяет информацию о вакансии по id.
    Необходимо передать id в path.
    """,
    summary="Данные о вакансии по id",
    response_model=VacanciesBase,
    status_code=status.HTTP_200_OK,
)
async def get_vacancies_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_vacancies: int,
) -> VacanciesBase:
    """
    ENDPOINT - Получение все вакансий.
    """

    logger.info(
        msg="Vacancy-Router вызов метода"
        " получения вакансии по "
        "id (get_vacancies_by_id)"
    )

    return await VacanciesService.get_vacancies_by_id(
        engine=session,
        id_vacancies=id_vacancies,
        redis_search_data="vacancies_data_by_id_%s" % id_vacancies,
    )


@vacancies_router.put(
    path="/update",
    description="""
    ### Endpoint - Обновление вакансии по id.
    Данный метод позволяет обновить информацию о вакансии по id.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Обновление информации о вакансии",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["AdminPanel - Панель администратора"],
)
async def update_vacancies(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    data_to_update: UpdateVacancies,
) -> None:
    """
    ENDPOINT - Обновление данных о вакансии.
    """

    logger.info(
        msg="Vacancy-Router вызов метода"
        " обновление вакансии по "
        "id (update_vacancies)"
    )

    return await VacanciesService.update_vacancies(
        engine=session, token=admin_data, data_to_update=data_to_update
    )


@vacancies_router.delete(
    path="/del/{id_vacancies}",
    description="""
    ### Endpoint - Удаление вакансии по id.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке.
    Необходим path id в ссылке запроса.
    """,
    summary="Удаление вакансии по id",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["AdminPanel - Панель администратора"],
)
async def delete_vacancies_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_vacancies: int,
) -> None:
    """
    ENDPOINT - Удаление вакансии.
    :session:
    :admin_data:
    :id_vacancies:
    """

    logger.info(
        msg="Vacancy-Router вызов метода" " удаления вакансии по id (delete_vacancies)"
    )

    return await VacanciesService.delete_vacancies_by_id(
        engine=session, token=admin_data, id_vacancies=id_vacancies
    )
