from fastapi import APIRouter, status, Depends
from typing import Annotated


# Local
from src.other.enums.api_enum import APIPrefix, APITagsEnum
from src.api.core.type_moto_app.schemas.type_moto_dto import (
    ListTypeModelBase,
)
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.api.core.type_moto_app.service.type_moto_service import (
    TypeMotoService,
)  # noqa


tm_router: APIRouter = APIRouter(
    prefix=APIPrefix.TYPE_MOTO.value, tags=[APITagsEnum.TYPE_MOTO.value]
)


@tm_router.get(
    path="/all",
    response_model=ListTypeModelBase,
    description="""
    ###  ENDPOINT - Получение всех типов транспорта
    Доступен всем
    """,
    status_code=status.HTTP_200_OK,
    summary="Все типы транспорта",
)
async def all_moto_types(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> ListTypeModelBase:
    """
    Все типы транспорта
    :param session:
    :return:
    """

    return await TypeMotoService.all_tm(engine=session, redis_search_data="all_tm")
