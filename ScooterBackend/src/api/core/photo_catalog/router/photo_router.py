from fastapi import APIRouter, status, Depends
from typing import Annotated
from src.api.core.photo_catalog.dto.photo_dto import AllPhotos, PhotoBase
from src.api.core.photo_catalog.service.photo_service import PhotoService
from src.api.dep.dependencies import EngineRepository, IEngineRepository
from src.other.enums.api_enum import APIPrefix, APITagsEnum


photo_router: APIRouter = APIRouter(
    prefix=APIPrefix.PHOTO_PREFIX.value, tags=[APITagsEnum.PHOTO.value]
)


@photo_router.get(
    path="/un_photo/{id_photo)",
    description="""
    Получение фотографии по идентификатору
    """,
    summary="Получение фотографии",
    status_code=status.HTTP_200_OK,
    response_model=PhotoBase,
)
async def get_photo_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_photo: int,
) -> PhotoBase:
    """
    API ROUTER: Получение фотографии продукта по идентификатору
    """

    return await PhotoService.get_photo_product_by_id(
        uow=engine,
        id_photo=id_photo,
        redis_search_data=f"photo_product_by_{id_photo}",
    )


@photo_router.get(
    path="/un_photo/product/{id_product}",
    description="""
    Получение всех фотографий продукта
    """,
    summary="Получение фотографий",
    status_code=status.HTTP_200_OK,
    response_model=AllPhotos,
)
async def get_photos_by_id_product(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_product: int,
) -> AllPhotos:
    """
    API ROUTER: Получение всех фотографий продукта по идентификатору продукта
    """

    return await PhotoService.get_all_photos_product(
        uow=engine,
        id_product=id_product,
        redis_search_data=f"all_photos_by_pr_{id_product}",
    )
