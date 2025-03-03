from fastapi import APIRouter, status, Depends
from src.api.core.mark_app.schemas.mark_dto import MarkBase, AllMarks
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.api.core.mark_app.service.mark_service import MarkService
from src.api.authentication.secure.authentication_service import Authentication
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from typing import Annotated, Dict, Union, List


mark_router: APIRouter = APIRouter(
    prefix=APIPrefix.MARK_PREFIX.value, tags=[APITagsEnum.MARK.value]
)
auth: Authentication = Authentication()


@mark_router.post(
    path="/create",
    description="""
    ### ENDPOINT - Создание марки.
    Доступен только для администратора
    """,
    summary="Создание марки",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def create_a_new_mark(
    admin_data: Annotated[Dict[str, str], Depends(auth.auth_user)],
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    new_mark: MarkBase,
) -> None:
    await MarkService.create_a_new_mark(
        token=admin_data, engine=engine, new_mark_data=new_mark
    )


@mark_router.get(
    path="/all",
    response_model=Union[List, AllMarks],
    description="""
    ### ENDPOINT - Получение списка всех имеющихся марок.
    """,
    summary="Получение всех марок",
    status_code=status.HTTP_200_OK,
)
async def get_all_marks(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> Union[List, AllMarks]:
    return await MarkService.get_all_marks(
        engine=engine, redis_search_data="all_marks"
    )


@mark_router.get(
    path="/unique/{id_mark}",
    description="""
    ### ENDPOINT - Получение марки по id.
    """,
    summary="Получение марки по id",
    response_model=MarkBase,
    status_code=status.HTTP_200_OK,
)
async def get_mark_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_mark: int,
) -> MarkBase:
    return await MarkService.get_mark_by_id(
        engine=engine,
        id_mark=id_mark,
        redis_search_data="mark_by_id_%s" % id_mark,
    )


@mark_router.delete(
    path="/delete/{id_mark}",
    description="""
    ### ENDPOINT - Удаление марки по id.
    Доступен только для администратора.
    """,
    summary="Удаление марки по id",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_mark_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_mark: int,
) -> None:
    await MarkService.delete_mark_by_id(engine=engine, id_mark=id_mark)
