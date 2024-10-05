from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.model_catalog.schemas.model_dto import ModelBase, AllModelBase
from src.api.core.model_catalog.service.model_service import ModelService
from typing import Annotated
from fastapi import APIRouter, status, Depends


auth: Authentication = Authentication()
model_router: APIRouter = APIRouter(
    prefix="/model",
    tags=["Model"]
)


@model_router.post(
    path="/create_new_model",
    response_model=None,
    description="""
    ### ENDPOINT - Метод для создания новой модели.
    Доступен только для администратора
    """,
    summary="Создание модели",
    status_code=status.HTTP_201_CREATED
)
async def create_new_model(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    new_model: ModelBase
) -> None:
    await ModelService.add_new_model(engine=engine, token=admin_data, new_model=new_model)


@model_router.get(
    path="/get_model_by_id/{id_model}",
    response_model=ModelBase,
    description="""
    ### ENDPOINT - Метод для получения данных о модели по идентификатору.
    """,
    summary="Получение модели по id",
    status_code=status.HTTP_200_OK
)
async def get_model_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_model: int
) -> ModelBase:
    return await ModelService.get_model_by_id(engine=engine, id_model=id_model)


@model_router.get(
    path="/get_all_models",
    response_model=AllModelBase,
    description="""
    ### ENDPOINT - Метод для получения всех моделей.
    """,
    summary="Получение всех моделей",
    status_code=status.HTTP_200_OK
)
async def get_all_models(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
) -> AllModelBase:
    return await ModelService.get_all_models(engine=engine, redis_search_data="all_models")


@model_router.delete(
    path="/delete_model_by_id/{id_model}",
    response_model=None,
    description="""
    ### ENDPOINT - Метод для удаления модели.
    Доступен только для администратора
    """,
    summary="Удаление модели",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_model_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_model: int
) -> None:
    await ModelService.delete_model_by_id(engine=engine, token=admin_data, id_model=id_model)