#System
from typing import Union, Annotated, Dict

#Other libraries
from pydantic import BaseModel, Field

#Local
from src.database.models.category import Category


class ReviewBase(BaseModel):

    text_review: Annotated[str, Field()]
    estimation_review: Annotated[int, Field(lt=11)]
    id_product: int


class ReviewMessage(BaseModel):

    text_review: Annotated[str, Field()]
    estimation_review: Annotated[int, Field(lt=11)]
    user_data: Dict[Union[str, int], Union[str, int]]


class AddReview(ReviewBase):
    pass


class DeleteReview(ReviewBase):
    id_review: Annotated[int, Field()]
    id_user: Annotated[int, Field()]


class ReviewIsDeleted(BaseModel):

    is_deleted: bool = False


class ReviewIsCreated(BaseModel):

    is_created: bool = False