from fastapi import APIRouter, status, Depends
from src.api.core.product_models_catalog.service.product_models_service import (
    ProductModelsService,
)
from src.api.core.product_models_catalog.schemas.product_models_dto import (
    ProductModelsBase,
    AllProductModels,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from typing import Annotated


auth: Authentication = Authentication()
product_models_router: APIRouter = APIRouter(
    prefix=APIPrefix.PRODUCT_MODEL_PREFIX.value,
    tags=[APITagsEnum.PRODUCT_MODEL.value],
)


@product_models_router.post(
    path="/create_new_product_models",
    response_model=None,
    description="""
    ### ENDPOINT - Добавление новой модели в продукт.
    Доступен только для администратора.
    """,
    summary="Добавление модели для продукта",
    status_code=status.HTTP_201_CREATED,
)
async def added_new_product_models(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    new_product_models: ProductModelsBase,
) -> None:
    await ProductModelsService.added_new_model_to_product(
        engine=engine, token=admin_data, new_model=new_product_models
    )


@product_models_router.get(
    path="/get_all_product_models_by_id_product/{id_product}",
    response_model=AllProductModels,
    description="""
    ### ENDPOINT - Получение все моделей продукта по идентификатору продукта.
    """,
    summary="Полученеи всех моделей продукта по id product",
    status_code=status.HTTP_200_OK,
)
async def get_all_product_models_by_id_pr(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_product: int,
) -> AllProductModels:
    return await ProductModelsService.get_model_by_id_product(
        engine=engine,
        id_product=id_product,
        redis_search_data="get_product_models_by_id_%s" % id_product,
    )


@product_models_router.get(
    path="/get_all_product_models",
    response_model=AllProductModels,
    description="""
    ### ENDPOINT - Получение всех моделей продуктов.
    """,
    summary="Получение списка всех моделей продуктов",
    status_code=status.HTTP_200_OK,
)
async def get_all_product_models(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
) -> AllProductModels:
    return await ProductModelsService.get_all_product_models(engine=engine)


@product_models_router.delete(
    path="/delete_product_models_by_id/{id_pr_model}",
    response_model=None,
    description="""
    ### ENDPOINT - Удаление модели продукта по идентификатору
    """,
    summary="Удаление модели продукта по идентификатору",
    status_code=status.HTTP_200_OK,
)
async def delete_product_model_by_id(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_pr_model: int,
) -> None:
    await ProductModelsService.delete_product_models_by_id(
        engine=engine, token=admin_data, id_pr_m=id_pr_model
    )
