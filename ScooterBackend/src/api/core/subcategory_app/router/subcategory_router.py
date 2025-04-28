from fastapi import APIRouter, status, Depends
from src.api.core.subcategory_app.service.subcategory_service import (
    SubCategoryService,
)
from src.api.core.subcategory_app.schemas.subcategory_dto import (
    SubCategoryBase,
    AllSubCategories,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from typing import Annotated


auth: Authentication = Authentication()
subcategory_router: APIRouter = APIRouter(
    prefix=APIPrefix.SUB_CATEGORY_PREFIX.value,
    tags=[APITagsEnum.SUB_CATEGORY.value],
)


@subcategory_router.post(
    path="/create",
    response_model=None,
    description="""
    ### ENDPOINT - Добавление новой подкатегории.
    Доступен только для администратора.
    """,
    summary="Добавление модели для продукта",
    status_code=status.HTTP_201_CREATED,
)
async def added_new_subcategory(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    new_subcategory: SubCategoryBase,
) -> None:
    await SubCategoryService.added_new_model_to_product(
        engine=engine, token=admin_data, new_model=new_subcategory
    )


@subcategory_router.get(
    path="/all/category/{id_category}",
    response_model=AllSubCategories,
    description="""
    ### ENDPOINT - Получение все моделей продукта по идентификатору продукта.
    """,
    summary="Получение всех моделей продукта по id product",
    status_code=status.HTTP_200_OK,
)
async def get_all_subcategories_by_id_category(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_category: int,
) -> AllSubCategories:
    return await SubCategoryService.get_subcategories_by_id_category(
        engine=engine,
        id_category=id_category,
        redis_search_data="get_subcategory_by_id_category_%s" % id_category,
    )


@subcategory_router.get(
    path="/all",
    response_model=AllSubCategories,
    description="""
    ### ENDPOINT - Получение всех подкатегорий.
    """,
    summary="Получение списка всех подкатегорий",
    status_code=status.HTTP_200_OK,
)
async def get_all_product_models(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
) -> AllSubCategories:
    return await SubCategoryService.get_all_product_models(engine=engine)


@subcategory_router.delete(
    path="/delete/{id_subcategory}",
    response_model=None,
    description="""
    ### ENDPOINT - Удаление подкатегори по идентификатору
    Доступен только для администратора
    """,
    summary="Удаление подкатегории по идентификатору",
    status_code=status.HTTP_200_OK,
)
async def delete_subcategory_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_subcategory: int,
) -> None:
    await SubCategoryService.delete_product_models_by_id(
        engine=engine, token=admin_data, id_subcategory=id_subcategory
    )
