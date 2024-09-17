# System
from typing import Union, Dict, List, Coroutine, Any, Type

# Other libraries
...

# Local
from src.database.models.review import Review
from src.api.exception.http_review_exception import *
from src.api.dto.review_dto import *
from src.api.exception.http_review_exception import ReviewHttpError
from src.api.exception.http_user_exception import UserHttpError
from src.api.authentication.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository


from src.store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()


class ReviewService:

    @staticmethod
    async def create_review(
        engine: IEngineRepository, token: str, new_review: ReviewBase
    ) -> ReviewIsCreated:
        """
        Метод сервиса для создания нового отзыва о товаре
        :param session:
        :param token:
        :param new_review:
        :return:
        """

        # Get user id
        token_data: Coroutine[Any, Any, Dict[str, str] | None] = (
            await Authentication().decode_jwt_token(token=token, type_token="access")
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

        async with engine:
            # Получение всех отзывов к товару
            all_reviews_for_product: Union[None, Review] = (
                await engine.review_repository.find_all_reviews_by_id_product(
                    id_product=id_product
                )
            )

            if all_reviews_for_product:
                reviews: ListReviewMessageForProduct = ListReviewMessageForProduct(
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
                            "user_name": review[0].user.read_model().get("name_user"),
                            "email_user": review[0].user.read_model().get("email_user"),
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

            await ReviewHttpError().http_review_not_found()

    @staticmethod
    async def delete_review(
        engine: IEngineRepository, id_review: int, token: str
    ) -> None:
        """
        Метод сервися для удаления отзыва.
        :param session:
        :param id_review:
        :param token:
        :return:
        """

        # Getting data
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(
            token=token, type_token="access"
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=jwt_data.get("email")
                )
            )

            if is_admin:
                is_review_deleted: bool = await engine.review_repository.delete_one(
                    other_id=id_review
                )
                if is_review_deleted:
                    return
                await ReviewHttpError().http_failed_to_delete_review()
            else:
                review_data: Union[None, Review] = (
                    await engine.review_repository.find_one(other_id=id_review)
                )
                if review_data:
                    if review_data[0].id_user == jwt_data.get("id_user"):
                        is_review_deleted: bool = (
                            await engine.review_repository.delete_one(
                                other_id=id_review
                            )
                        )
                        if is_review_deleted:
                            return
                        await ReviewHttpError().http_failed_to_delete_review()
                    await UserHttpError().http_user_not_found()
                await ReviewHttpError().http_review_not_found()
