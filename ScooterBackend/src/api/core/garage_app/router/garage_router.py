from fastapi import APIRouter, status, Depends
from typing import Annotated, Dict


# Local
from src.other.enums.api_enum import (
    APITagsEnum, APIPrefix
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import (
    IEngineRepository,
    EngineRepository
)
from src.api.core.garage_app.schemas.garage_dto import (
    ListGarageBase,
    GarageBase
)
from src.api.core.garage_app.service.garage_service import GarageService


garage_router: APIRouter = APIRouter(
    prefix=APIPrefix.GARAGE_PREFIX.value,
    tags=[APITagsEnum.GARAGE.value]
)
auth: Authentication = Authentication()


@garage_router.get(
    path="/all",
    description="""
    ### ENDPOINT -  Получение всего гаража пользователя""",
    summary="Гараж пользователя",
    response_model=ListGarageBase,
    status_code=status.HTTP_200_OK
)
async def my_garage(
        engine: Annotated[IEngineRepository, Depends(EngineRepository)],
        user_data: Annotated[str, Depends(auth.auth_user)],
) -> ListGarageBase:
    """
    Получение пользовательского гаража
    :param engine:
    :param user_data:
    :return:
    """

    return await GarageService.get_user_mt_from_garage(engine=engine, token=user_data)
