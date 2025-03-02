# System
from typing import Annotated, List, Type, Union
import logging

# Other libraries
from fastapi import Depends, status, APIRouter

# Local
from src.api.core.review_app.schemas.review_dto import (
    ReviewBase,
    ReviewMessage,
    ListReviewMessageForProduct,
    ReviewIsCreated,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.review_app.service.review_service import ReviewService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix


review_router: APIRouter = APIRouter(
    prefix=APIPrefix.REVIEW_PREFIX.value, tags=[APITagsEnum.REVIEW.value]
)

auth: Authentication = Authentication()
logger: Type[logging.Logger] = logging.getLogger(__name__)


@review_router.post(
    path="/create",
    description="""
    ### Endpoint - Создание отзыва.
    Данный метод позволяет создать новый отзыв.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Create review",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewIsCreated,
)
async def create_review(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(auth.auth_user)],
    new_review: ReviewBase,
) -> ReviewIsCreated:
    """
    ENDPOINT - Создание нового отзыва
    :param session:
    :param usr_data:
    :param new_review:
    :return:
    """

    logger.info(
        msg="Review-Router вызов " "метода создания отзыва (create_review)"
    )

    return await ReviewService.create_review(
        engine=session, token=user_data, new_review=new_review
    )


@review_router.get(
    path="/all/product/{id_product}",
    description="""
    ### Endpoint - Получение всех отзывов для товара.
    Данный метод позволяет получить список всех отзывов по id продукта.
    """,
    summary="Список отзывов по id",
    response_model=ListReviewMessageForProduct,
    status_code=status.HTTP_200_OK,
)
async def get_all_reviews_by_id_product(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    id_product: int,
) -> ListReviewMessageForProduct:
    """
    ENDPOINT - Получение всех комментариев к указанному товару.
    :param session:
    :param id_product:
    :return:
    """

    logger.info(
        msg="Review-Router вызов метода "
        "получения всех отзывов по "
        "id продукта (get_all_reviews_by_id_product)"
    )

    return await ReviewService.get_all_reviews_by_id_product(
        engine=session,
        id_product=id_product,
        redis_search_data="get_all_reviews_for_product_by_id_%s" % id_product,
    )


@review_router.get(
    path="/all",
    description="""
    ### Endpoint - Получение всех отзывов.
    Данный метод возвращает все отзывы продуктов.
    """,
    summary="Все отзывы",
    status_code=status.HTTP_200_OK,
    response_model=Union[List, List[ReviewMessage]],
)
async def get_all_reviews(
    session: Annotated[IEngineRepository, Depends(EngineRepository)]
) -> Union[List, List[ReviewMessage]]:
    """
    ENDPOINT - Возвращает список отзывов
    :param session:
    :return:
    """

    logger.info(
        msg="Review-Router вызов метода "
        "получение всех отзывов (get_all_reviews)"
    )

    return await ReviewService.get_all_reviews(engine=session)


@review_router.get(
    path="/unique/{review_id}",
    description="""
    ### Endpoint - Получение отзыва по id.
    Данный метод позволяет получить данные с отзыва по id.
    Необходимо передать id отзыва в ссылку.
    """,
    summary="Получение отзыва по id",
    status_code=status.HTTP_200_OK,
    response_model=ReviewMessage,
)
async def get_review_data_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    review_id: int,
) -> ReviewMessage:
    """
    ENDPOINT - Получение отзыва по id
    :param session:
    :param review_id:
    :return:
    """

    logger.info(
        msg="Review-Router вызов метода получения отзыва"
        " по id (get_review_data_by_id)"
    )

    return await ReviewService.get_review_by_id(
        engine=session,
        review_id=review_id,
        redis_search_data="review_by_id_%s" % review_id,
    )


@review_router.delete(
    path="/delete/{id_review}",
    description="""
    ### Endpoint - Удаление отзыва.
    Данный метод позволяет удалить отзыв.
    Отзыв может удалить либо создатель, либо администратор!
    """,
    summary="Удаление отзыва",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    tags=["AdminPanel - Панель администратора"],
)
async def delete_review_by_id(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    admin_data: Annotated[str, Depends(auth.auth_user)],
    id_review: int,
) -> None:
    """
    ENDPOINT - Удаление отзыва
    :param session:
    :param usr_data:
    :param id_review:
    :return:
    """

    logger.info(
        msg="Review-Router вызов метода"
        " удаления отзыва по id (delete_review_by_id)"
    )

    return await ReviewService.delete_review(
        engine=session, token=admin_data, id_review=id_review
    )
