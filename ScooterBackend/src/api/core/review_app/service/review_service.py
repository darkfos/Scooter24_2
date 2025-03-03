# System
from typing import Type, Union, List
import logging as logger


# Local
from database.models.review import Review
from api.core.review_app.schemas.review_dto import (
    ReviewMessage,
    ReviewBase,
    ReviewIsCreated,
    ListReviewMessageForProduct,
)
from api.core.review_app.error.http_review_exception import (
    ReviewHttpError,
)
from api.core.user_app.error.http_user_exception import UserHttpError
from api.authentication.secure.authentication_service import Authentication
from api.dep.dependencies import IEngineRepository
from other.enums.auth_enum import AuthenticationEnum


from store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class ReviewService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_review(
        engine: IEngineRepository,
        token: str,
        new_review: ReviewBase,
        token_data: dict = dict(),
    ) -> ReviewIsCreated:
        """
        Метод сервиса для создания нового отзыва о товаре
        :param session:
        :param token:
        :param new_review:
        :return:
        """

        logging.info(
            msg=f"{ReviewService.__name__} " f"Создание нового отзыва о товаре"
        )

        async with engine:
            # Created new review
            is_created: bool = await engine.review_repository.add_one(
                data=Review(
                    text_review=new_review.text_review,
                    estimation_review=new_review.estimation_review,
                    id_user=token_data.get("id_user"),
                    id_product=new_review.id_product,
                )
            )

            return ReviewIsCreated(is_created=is_created)

    @redis
    @staticmethod
    async def get_all_reviews_by_id_product(
        engine: IEngineRepository, id_product: int, redis_search_data: str
    ) -> Union[List, List[ReviewMessage]]:
        """
        Метод сервиса для получения списка комментариев к указанному товару.
        :param session:
        :param id_product:
        :return:
        """

        logging.info(
            msg=f"{ReviewService.__name__} "
            f"Получение списка комментариев к указанному "
            f"товару id_product={id_product}"
        )
        async with engine:
            # Получение всех отзывов к товару
            all_reviews_for_product: Union[None, Review] = (
                await engine.review_repository.find_all_reviews_by_id_product(
                    id_product=id_product
                )
            )

            if all_reviews_for_product:
                reviews: ListReviewMessageForProduct = (
                    ListReviewMessageForProduct(
                        reviews=[
                            ReviewMessage(
                                text_review=review[0].text_review,
                                estimation_review=review[0].estimation_review,
                                user_data={
                                    "user_name": review[0]
                                    .user.read_model()
                                    .get("name_user"),
                                    "email_user": review[0]
                                    .user.read_model()
                                    .get("email_user"),
                                },
                            )
                            for review in all_reviews_for_product
                        ]
                    )
                )

                return reviews

            return ListReviewMessageForProduct(reviews=[])

    @staticmethod
    async def get_all_reviews(
        engine: IEngineRepository,
    ) -> Union[List, List[ReviewMessage]]:
        """
        Метод сервиса который возвращает список всех имеющихся отзывов
        :param session:
        :return:
        """

        logging.info(
            msg=f"{ReviewService.__name__} "
            f"Получение списка имеющихся товаров"
        )
        async with engine:
            # Получение всех отзывов к товару
            all_reviews: Union[None, Review] = (
                await engine.review_repository.find_all_reviews_with_user_data()
            )

            if all_reviews:
                return [
                    ReviewMessage(
                        text_review=review[0].text_review,
                        estimation_review=review[0].estimation_review,
                        user_data={
                            "user_name": review[0]
                            .user.read_model()
                            .get("name_user"),  # noqa
                            "email_user": review[0]
                            .user.read_model()
                            .get("email_user"),  # noqa
                        },
                    )
                    for review in all_reviews
                ]

            return all_reviews

    @redis
    @staticmethod
    async def get_review_by_id(
        engine: IEngineRepository, review_id: int, redis_search_data: str
    ) -> ReviewMessage:
        """
        Метод сервиса для получения данных об отзыве через id.
        :param session:
        :param review_id:
        :return:
        """

        logging.info(
            msg=f"{ReviewService.__name__} "
            f"Получение данных об отзыве по id={review_id}"
        )
        async with engine:
            review_data = (
                await engine.review_repository.find_all_reviews_with_user_data(
                    id_review=review_id
                )
            )
            if review_data:
                return ReviewMessage(
                    text_review=review_data[0][0].text_review,
                    estimation_review=review_data[0][0].estimation_review,
                    user_data={
                        "user_name": review_data[0][0]
                        .user.read_model()
                        .get("name_user"),
                        "email_user": review_data[0][0]
                        .user.read_model()
                        .get("email_user"),
                    },
                )
            logging.critical(
                msg=f"{ReviewService.__name__} " f"Не удалось найти отзыв"
            )
            await ReviewHttpError().http_review_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_review(
        engine: IEngineRepository,
        id_review: int,
        token: str,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервися для удаления отзыва.
        :param session:
        :param id_review:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{ReviewService.__name__} "
            f"Удаление отзыва по id_review={id_review}"
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                is_review_deleted: bool = (
                    await engine.review_repository.delete_one(
                        other_id=id_review
                    )
                )
                if is_review_deleted:
                    return
                await ReviewHttpError().http_failed_to_delete_review()
            else:
                review_data: Union[None, Review] = (
                    await engine.review_repository.find_one(other_id=id_review)
                )
                if review_data:
                    if review_data[0].id_user == token_data.get("id_user"):
                        is_review_deleted: bool = (
                            await engine.review_repository.delete_one(
                                other_id=id_review
                            )
                        )
                        if is_review_deleted:
                            return
                        logging.critical(
                            msg=f"{ReviewService.__name__} "
                            f"Не удалось удалить отзыв"
                        )
                        await ReviewHttpError().http_failed_to_delete_review()
                    logging.critical(
                        msg=f"{ReviewService.__name__} "
                        f"Не удалось удалить отзыв,"
                        f" пользователь"
                        f" не был найден"
                    )
                    await UserHttpError().http_user_not_found()
                logging.critical(
                    msg=f"{ReviewService.__name__} "
                    f"Не удалось удалить отзыв, отзыв"
                    f" не был найден"
                )
                await ReviewHttpError().http_review_not_found()
