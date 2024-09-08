#System
from typing import Annotated, List

#Other libraries
from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from src.api.dto.review_dto import *
from src.database.db_worker import db_work
from src.api.authentication.authentication_service import Authentication
from src.api.service.review_service import ReviewService
from src.api.dep.dependencies import IEngineRepository, EngineRepository


review_router: APIRouter = APIRouter(
    prefix="/review",
    tags=["Review - Отзывы товаров, магазина"]
)

auth: Authentication = Authentication()


@review_router.post(
    path="/create_new_review",
    description="""
    ### Endpoint - Создание отзыва.
    Данный метод позволяет создать новый отзыв.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Create review",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewIsCreated
)
async def create_review(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.jwt_auth)],
    new_review: ReviewBase
) -> ReviewIsCreated:
    """
    ENDPOINT - Создание нового отзыва
    :param session:
    :param usr_data:
    :param new_review:
    :return:
    """

    return await ReviewService.create_review(engine=session, token=user_data, new_review=new_review)


@review_router.get(
    path="/get_all_reviews/{id_product}",
    description="""
    ### Endpoint - Получение всех отзывов для товара.
    Данный метод позволяет получить список всех отзывов по id продукта.
    """,
    summary="Список отзывов по id",
    response_model=List[ReviewMessage],
    status_code=status.HTTP_200_OK
)
async def get_all_reviews_by_id_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_product: int
) -> Union[List, List[ReviewMessage]]:
    """
    ENDPOINT - Получение всех комментариев к указанному товару.
    :param session:
    :param id_product:
    :return:
    """

    return await ReviewService.get_all_reviews_by_id_product(engine=session, id_product=id_product)


@review_router.get(
    path="/get_all_reviews",
    description="""
    ### Endpoint - Получение всех отзывов.
    Данный метод возвращает все отзывы продуктов.
    """,
    summary="Все отзывы",
    status_code=status.HTTP_200_OK,
    response_model=Union[List, List[ReviewMessage]]
)
async def get_all_reviews(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> Union[List, List[ReviewMessage]]:
    """
    ENDPOINT - Возвращает список отзывов
    :param session:
    :return:
    """

    return await ReviewService.get_all_reviews(engine=session)


@review_router.get(
    path="/get_review_by_id/{review_id}",
    description="""
    ### Endpoint - Получение отзыва по id.
    Данный метод позволяет получить данные с отзыва по id.
    Необходимо передать id отзыва в ссылку.
    """,
    summary="Получение отзыва по id",
    status_code=status.HTTP_200_OK,
    response_model=ReviewMessage
)
async def get_review_data_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    review_id: int
) -> ReviewMessage:
    """
    ENDPOINT - Получение отзыва по id
    :param session:
    :param review_id:
    :return:
    """

    return await ReviewService.get_review_by_id(engine=session, review_id=review_id)


@review_router.delete(
    path="/delete_my_review/{id_review}",
    description="""
    ### Endpoint - Удаление отзыва.
    Данный метод позволяет удалить отзыв.
    Отзыв может удалить либо создатель, либо администратор!
    """,
    summary="Удаление отзыва",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    tags=["AdminPanel - Панель администратора"]
)
async def delete_review_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.jwt_auth)],
    id_review: int,
) -> None:
    """
    ENDPOINT - Удаление отзыва
    :param session:
    :param usr_data:
    :param id_review:
    :return:
    """

    return await ReviewService.delete_review(
        engine=session, token=admin_data, id_review=id_review
    )