#System
from typing import Annotated

#Other libraries
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.api.dto.admin_dto import (
    AdminBase,
    AdminIsCreated
)
from ScooterBackend.api.service.admin_service import AdminService
from ScooterBackend.database.db_worker import db_work

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
    session: Annotated[AsyncSession, Depends(db_work.get_session)],
    new_admin: AdminBase
) -> AdminIsCreated:
    """
    Создание нового администратора
    :return:
    """

    return await AdminService.create_admin(session=session, new_admin=new_admin)