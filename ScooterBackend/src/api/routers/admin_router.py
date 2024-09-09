#System
from typing import Annotated

#Other libraries
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from src.api.dto.admin_dto import (
    AdminBase,
    AdminIsCreated
)
from src.api.service.admin_service import AdminService
from src.database.db_worker import db_work
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.api.authentication.authentication_service import Authentication

admin_router: APIRouter = APIRouter(
    prefix="/admin",
    tags=["AdminPanel - Панель администратора"]
)


@admin_router.post(
    path="/create_admin",
    description="""
    ### Endpoint - Создание администратора.
    Данный метод позволяет создать нового пользователя с ролью администратора.
    """,
    summary="Создание администратора",
    response_model=AdminIsCreated,
    status_code=status.HTTP_201_CREATED
)
async def create_admin(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(Authentication().jwt_auth)],
    new_admin: AdminBase
) -> AdminIsCreated:
    """
    Создание нового администратора
    :return:
    """

    return await AdminService.create_admin(engine=session, new_admin=new_admin, user_data=user_data)