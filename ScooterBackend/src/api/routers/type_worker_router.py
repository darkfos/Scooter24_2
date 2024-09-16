#System
from typing import Annotated, List, Union


#Other libraries
from fastapi import APIRouter, status, Depends


#Local
from src.api.service.type_worker_service import TypeWorkerService
from src.api.authentication.authentication_service import Authentication
from src.api.dto.type_worker_dto import TypeWorkerBase, TypeWorkerList
from src.api.dep.dependencies import IEngineRepository, EngineRepository


auth: Authentication = Authentication()
type_worker_router: APIRouter = APIRouter(
    prefix="/type_worker",
    tags=["TypeWorker - Тип работников"]
)


@type_worker_router.post(
    path="/create_new_type_worker",
    description="""
    ### Endpoint - Создание нового типа работника для вакансий.
    Необходим jwt ключ и Bearer в заголовке запроса.
    Доступен только для администратора.
    """,
    summary="Создание типа работника",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["AdminPanel - Панель администратора"]
)
async def create_new_type_worker(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    new_type_worker: TypeWorkerBase
) -> None:
    """
    ENDPOINT - Создание нового типа работникаю
    :session:
    :admin_data:
    :new_type_worker:
    """

    return await TypeWorkerService.create_a_new_type_worker(
        engine=session,
        token=admin_data,
        new_type_worker=new_type_worker
    )


@type_worker_router.get(
    path="/get_all_types_workers",
    description="""### Endpoint - Получение всех типов работников.""",
    summary="Все типы работников",
    response_model=TypeWorkerList,
    status_code=status.HTTP_200_OK
)
async def get_all_types_workers(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> TypeWorkerList:
    """
    ENDPOINT - Получение всех типов работников.
    """

    return await TypeWorkerService.get_all_types(
        engine=session,
        redis_search_data="get_all_types_workers"
    )


@type_worker_router.get(
    path="/get_type_worker_by_id",
    description="""Получение типов работников по id.
    Необходимо передать id типа работника в query параметры""",
    summary="Поиск типа работника по id",
    response_model=TypeWorkerBase,
    status_code=status.HTTP_200_OK
)
async def get_type_worker_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_type_worker: int
) -> TypeWorkerBase:
    return await TypeWorkerService.get_type_worker_by_id(
        engine=session,
        id_type_worker=id_type_worker,
        redis_search_data="type_worker_by_id_%s" % id_type_worker
    )


@type_worker_router.delete(
    path="/delete_type_worker_by_id",
    description="""
    Endpoint - Удаление типа работника по id.
    Данный метод доступен только для администраторов!
    Необходим jwt ключ и Bearer в заголовке запроса, а также id_type в query параметрах.
    """,
    summary="Удаление типа работника",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_type_worker(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_type: int,
) -> None:
    """
    ENDPOINT - Удаление типа работника
    """

    return await TypeWorkerService.delete_type_worker(engine=session, id_type_worker=id_type, token=admin_data)