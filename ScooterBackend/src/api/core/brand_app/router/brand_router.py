from fastapi import APIRouter, status, Depends, UploadFile
from api.core.brand_app.service.brand_service import BrandService
from api.dep.dependencies import IEngineRepository, EngineRepository
from api.authentication.secure.authentication_service import Authentication
from pydantic import Field
from api.core.brand_app.schemas.brand_dto import (
    BrandBase,
    AllBrands,
)
from other.enums.api_enum import APITagsEnum, APIPrefix
from typing import Annotated


brand_router = APIRouter(
    prefix=APIPrefix.BRAND_PREFIX.value, tags=[APITagsEnum.BRAND.value]
)
auth: Authentication = Authentication()


@brand_router.post(
    path="/create",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
    ### ENDPOINT - Создание нового бренда,
    Доступен только для администратора.
    """,
    summary="Создание нового бренда",
)
async def create_a_new_brand(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    name_brand: Annotated[str, Field(max_length=100)],
    photo: UploadFile,
) -> None:
    await BrandService.add_a_new_brand(
        engine=engine, token=admin_data, name_brand=name_brand, photo=photo
    )


@brand_router.get(
    path="/one/{id_brand}",
    response_model=BrandBase,
    status_code=status.HTTP_200_OK,
    description="""
    ### ENDPOINT - Получение бренда по идентификатору.
    """,
    summary="Получение бренда по идентификатору",
)
async def get_brand_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_brand: int,
) -> BrandBase:
    return await BrandService.get_brand_by_id(
        engine=engine,
        id_brand=id_brand,
        redis_search_data="get_brand_by_id_%s" % id_brand,
    )


@brand_router.get(
    path="/all",
    response_model=AllBrands,
    status_code=status.HTTP_200_OK,
    description="""
    ### ENDPOINT - Получение списка брендов.
    """,
    summary="Получение списка брендов",
)
async def get_all_brands(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> AllBrands:
    return await BrandService.get_all_brands(
        engine=engine, redis_search_data="get_all_brands"
    )


@brand_router.delete(
    path="/delete/{id_brand}",
    response_model=None,
    description="""
    ### ENDPOINT - Удаление бренда по идентификатору.
    Доступен только для администратора.
    """,
    summary="Удаление бренда по идентификатору",
    status_code=status.HTTP_200_OK,
)
async def delete_brand_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_brand: int,
) -> None:
    await BrandService.delete_brand_by_id(
        engine=engine, token=admin_data, id_brand=id_brand
    )
