from fastapi import APIRouter, status, Depends
from typing import Annotated, Dict


# Local
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.api.core.garage_app.schemas.garage_dto import (
    ListGarageBase,
    AddNewMotoToGarage,
)
from src.api.core.garage_app.service.garage_service import GarageService


garage_router: APIRouter = APIRouter(
    prefix=APIPrefix.GARAGE_PREFIX.value, tags=[APITagsEnum.GARAGE.value]
)
auth: Authentication = Authentication()


@garage_router.post(
    path="/create",
    description="""
    ### ENDPOINT - Добавление транспорта в гараж
    """,
    summary="Добавление в гараж",
    response_model=Dict[str, int],
    status_code=status.HTTP_201_CREATED,
)
async def added_garage(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    new_mt: AddNewMotoToGarage,
) -> Dict[str, int]:
    """
    Добавление нового транспорта в гараж

    :param engine:
    :param user_data:
    :param new_mt:
    :return:
    """

    return {
        "id_garage": await GarageService.create_moto_in_garage(
            engine=engine, token=user_data, new_moto=new_mt
        )
    }


@garage_router.get(
    path="/all",
    description="""
    ### ENDPOINT -  Получение всего гаража пользователя""",
    summary="Гараж пользователя",
    response_model=ListGarageBase,
    status_code=status.HTTP_200_OK,
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


@garage_router.delete(
    path="/delete",
    description="""
    ## ENDPOINT - Удаление мототранспорта из гаража
    Доступен только пользователю
    """,
    response_model=None,
    summary="Удаление транспорта с гаража",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_transport(
    user_data: Annotated[str, Depends(auth.auth_user)],
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_mt: int,
) -> None:
    """
    Удаление мототранспорта из гаража пользователя
    :param user_data:
    :param engine:
    :param id_mt:
    :return:
    """

    return await GarageService.delete_mt(token=user_data, engine=engine, id_mt=id_mt)
