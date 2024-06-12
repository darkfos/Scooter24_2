#System
from typing import Annotated, List, Union

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, Depends, APIRouter

#Local
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.api.dto.vacancies_dto import VacanciesBase, UpdateVacancies
from ScooterBackend.database.db_worker import db_work
from ScooterBackend.api.service.vacancies_service import VacanciesService


auth: Authentication = Authentication()
vacancies_router: APIRouter = APIRouter(
    prefix="/vacancies",
    tags=["Vacancies - Вакансии"]
)


@vacancies_router.post(
    path="/create_new_vacancies",
    description="""
    ### Endpoint - создание новой вакансии.
    Данный метод позволяет создать новую вакансию.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Создание вакансии",
    response_model=None,
    status_code=status.HTTP_200_OK,
    tags=["AdminPanel - Панель администратора"]
)
async def create_a_new_vacancies(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    new_vacancies: VacanciesBase
) -> None:
    """
    ENDPOINT - Создание новой вакансии
    :session:
    :admin_data:
    :new_vacancies:
    """

    return await VacanciesService.create_vacancies(
        session=session,
        token=admin_data,
        vac_data=new_vacancies
    )


@vacancies_router.get(
    path="/get_all_vacancies",
    description="""
    ### Endpoint - Получение всех вакансий.
    Данный метод позволяет получить все вакансии.
    """,
    summary="Список всех вакансий",
    response_model=Union[List, List[VacanciesBase]],
    status_code=status.HTTP_200_OK
)
async def get_all_vacancies(
    session: Annotated[AsyncSession, Depends(db_work.get_session)]
) -> Union[List, List[VacanciesBase]]:
    """
    ENDPOINT - Получение все вакансий.
    """

    return await VacanciesService.get_all_vacancies(session=session)


@vacancies_router.get(
    path="/get_vacancies_by_id/{id_vacancies}",
    description="""
    ### Endpoint - Получение вакансии по id.
    Данный метод позволяет информацию о вакансии по id.
    Необходимо передать id в path.
    """,
    summary="Данные о вакансии по id",
    response_model=VacanciesBase,
    status_code=status.HTTP_200_OK
)
async def get_all_vacancies(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    id_vacancies: int
) -> VacanciesBase:
    """
    ENDPOINT - Получение все вакансий.
    """

    return await VacanciesService.get_vacancies_by_id(session=session)


@vacancies_router.put(
    path="/update_vacancies",
    description="""
    ### Endpoint - Обновление вакансии по id.
    Данный метод позволяет обновить информацию о вакансии по id.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Обновление информации о вакансии",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["AdminPanel - Панель администратора"]
)
async def get_all_vacancies(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    data_to_update: UpdateVacancies
) -> None:
    """
    ENDPOINT - Получение все вакансий.
    """

    return await VacanciesService.update_vacancies(
        session=session,
        token=admin_data,
        data_to_update=data_to_update
    )


@vacancies_router.delete(
    path="/delete_vacancies/{id_vacancies}",
    description="""
    ### Endpoint - Удаление вакансии по id.
    Доступен только для администраторов.
    Необходим jwt ключ и Bearer в заголовке.
    Необходим path id в ссылке запроса.
    """,
    summary="Удаление вакансии по id",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["AdminPanel - Панель администратора"]
)
async def delete_vacancies_by_id(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_vacancies: int
) -> None:
    """
    ENDPOINT - Удаление вакансии.
    :session:
    :admin_data:
    :id_vacancies:
    """

    return await VacanciesService.delete_vacancies_by_id(
        session=session,
        token=admin_data,
        id_vacancies=id_vacancies
    )