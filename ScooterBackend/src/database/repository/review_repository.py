# System
from typing import Union, List, Type
import logging as logger

# Other
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, Result
from sqlalchemy.orm import joinedload

# Local
from src.database.models.review import Review
from src.database.repository.general_repository import GeneralSQLRepository


logging = logger.getLogger(__name__)


class ReviewRepository(GeneralSQLRepository):

    def __init__(self, session: AsyncSession):
        self.model: Type[Review] = Review
        super().__init__(session=session, model=self.model)

    async def del_more(self, id_reviews: List[int]) -> bool:
        """
        Удаление нескольких отзывов
        :param args:
        :param kwargs:
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} Удаление отзывов id_reviews={id_reviews}")
        for id_review in id_reviews:
            delete_review = delete(Review).where(Review.id == id_review)
            await self.async_session.execute(delete_review)
            await self.async_session.commit()

        return True

    async def find_all_reviews_by_id_product(
        self, id_product: int
    ) -> Union[List, List[Review]]:
        """
        Получение всех отзывов к продукту
        :param id_product:
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} Поиск всех отзывов к продукту id_product={id_product}")
        stmt = (
            select(Review)
            .where(Review.id_product == id_product)
            .options(joinedload(Review.user))
        )
        reviews = ((await self.async_session.execute(stmt)).unique()).fetchall()

        return reviews

    async def find_all_reviews_with_user_data(
        self, id_review: Union[int, None] = None
    ) -> Union[List, List[Review]]:
        """
        Получение всех отзывов с данными о пользователях
        :return:
        """

        logging.info(msg=f"{self.__class__.__name__} Получение всех отзывов с данными о пользователях id_review={id_review}")

        if id_review:
            stmt = (
                select(Review)
                .where(Review.id == id_review)
                .options(joinedload(Review.user))
            )
        else:
            stmt = select(Review).options(joinedload(Review.user))

        reviews = ((await self.async_session.execute(stmt)).unique()).fetchall()

        return reviews
