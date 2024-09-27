# System
from typing import Annotated
import logging

# Other libraries
from fastapi import APIRouter, status, Depends, Request

# Local
from src.api.core.admin_catalog.schemas.admin_dto import AdminBase, AdminIsCreated
from src.api.core.admin_catalog.service.admin_service import AdminService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.api.authentication.secure.authentication_service import Authentication

admin_router: APIRouter = APIRouter(
    prefix="/admin", tags=["AdminPanel - Панель администратора"]
)
logger = logging.getLogger(__name__)


@admin_router.post(
    path="/create_admin",
    description="""
    ### Endpoint - Создание администратора.
    Данный метод позволяет создать нового пользователя с ролью администратора.
    """,
    summary="Создание администратора",
    response_model=AdminIsCreated,
    status_code=status.HTTP_201_CREATED,
)
async def create_admin(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(Authentication().jwt_auth)],
    new_admin: AdminBase,
) -> AdminIsCreated:
    """
    Создание нового администратора
    :return:
    """
    
    logger.info(msg="ADMIN-ROUTER вызов метода создания администратора (create_admin)")
    return await AdminService.create_admin(
        engine=session, new_admin=new_admin, token=user_data
    )


@admin_router.get(
    path="/load_data/{model}",
    description="""
    ENDPOINT - Загрузка csv, .xlsx данных в админ панели
    """,
    status_code=status.HTTP_200_OK
)
async def load_data_in_model(request: Request, model: str):
    print(request, model)