from fastapi import APIRouter, status, Depends
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.user_type_catalog.service.user_type_service import UserTypeService, NewUserType, AllUserType
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from typing import Annotated


user_type_router: APIRouter = APIRouter(
    prefix="/user_type",
    tags=["User Type"]
)

auth: Authentication = Authentication()


@user_type_router.post(
    path="/create_user_type",
    description="""
    ### ENDPOINT - создание типа пользователя,
    Доступен только для администратора
    """,
    summary="Создание типа пользователя",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user_type(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    new_user_type: NewUserType
) -> None:
    await UserTypeService.create_user_type(engine=engine, token_data=admin_data, new_user_type=new_user_type)


@user_type_router.get(
    path="/get_all_user_types",
    description="""
    ### ENDPOINT - получение всех типов пользователей""",
    summary="Все типы пользователей",
    response_model=AllUserType,
    status_code=status.HTTP_200_OK
)
async def all_user_types(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> AllUserType:
    return await UserTypeService().get_all_user_types(engine=engine)