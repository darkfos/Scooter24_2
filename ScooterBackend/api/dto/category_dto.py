#Other libraries
from pydantic import Field, BaseModel
from typing import List, Union, Annotated

#Local
...


class CategoryBase(BaseModel):
    """
    Базовый DTO для категорий
    """

    name_category: Annotated[str, Field(max_length=150)]


class CategoryIsCreated(BaseModel):

    is_created: bool


class CategoryIsFinded(BaseModel):

    is_find: bool


class DataCategoryToUpdate(BaseModel):

    name_category: str
    new_name_category: str


class CategoryIsUpdated(BaseModel):

    is_updated: bool