#System
from typing import Annotated


#Other libraries
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession


#Local
from ScooterBackend.api.service.type_worker_service import TypeWorkerService
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.database.db_worker import db_work
from ScooterBackend.api.dto.type_worker_dto import TypeWorkerBase


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
    status_code=status.HTTP_204_NO_CONTENT
)
async def create_new_type_worker(
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
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
        session=session,
        token=admin_data,
        new_type_worker=new_type_worker
    )