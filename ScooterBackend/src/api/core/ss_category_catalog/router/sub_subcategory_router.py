from fastapi import APIRouter, status, Depends
from src.api.core.ss_category_catalog.service.sub_subcategories_service import SubSubCategoryService
from src.api.core.ss_category_catalog.schemas.sub_subcategory_dto import AllSubSubCategory, SubSubCategoryBase
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from typing import Annotated


auth: Authentication = Authentication()
ss_category_router: APIRouter = APIRouter(
    prefix=APIPrefix.SSUB_CATEGORY_PREFIX.value,
    tags=[APITagsEnum.SSUB_CATEGORY.value]
)


@ss_category_router.post(
    path="/create_new_sub_s_category",
    response_model=None,
    description="""
    ### ENDPOINT - Создание новой под подкатегории.
    Доступен только для администратора.
    """,
    summary="Создание под-подкатегории",
    status_code=status.HTTP_204_NO_CONTENT
)
async def create_a_new_sub_subcategory(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    new_sub_subcategory: SubSubCategoryBase
) -> None:
    await SubSubCategoryService.create_new_sub_subcategory(engine=engine, token=admin_data, new_s_sc=new_sub_subcategory)


@ss_category_router.get(
    path="/get_sub_subcategories_by_id_sc/{id_sc}",
    response_model=AllSubSubCategory,
    description="""
    ### ENDPOINT - Получение всех подкатегорий по подкатегории 1-го уровня
    """,
    summary="Получение подкатегорий 2-го уровня по подкатегории 1-го уровня",
    status_code=status.HTTP_200_OK
)
async def get_all_ss_category_by_subcategory(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_sc: int
) -> AllSubSubCategory:
    return await SubSubCategoryService.get_sub_subcategory_by_id_s(engine=engine, id_s=id_sc, redis_search_data="get_all_subcategories_by_id_%s" % id_sc)


@ss_category_router.get(
    path="/get_all_sscategories",
    response_model=AllSubSubCategory,
    description="""
    ### ENDPOINT - Получение всех подкатегорий.
    """,
    summary="Получение всех подкатегорий",
    status_code=status.HTTP_200_OK
)
async def get_all_subcategories(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> AllSubSubCategory:
    return await SubSubCategoryService.get_all_sub_subcategory(engine=engine, redis_search_data="get_all_sub_subcategories")


@ss_category_router.delete(
    path="/delete_sub_subcategory/{id_ss_category}",
    response_model=None,
    description="""
    ### ENDPOINT - Удаление подкатегории по идентификатору.
    Доступен только для администратора.
    """,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление подкатегории по подкатегории"
)
async def delete_sscategory_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_ss_category: int,
) -> None:
    await SubSubCategoryService.delete_sub_subcategory_by_id(engine=engine, token=admin_data, id_s_sc=id_ss_category)