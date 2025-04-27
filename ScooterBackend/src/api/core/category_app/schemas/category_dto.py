# Other libraries
from pydantic import Field, BaseModel
from typing import List, Annotated

# Local
from src.api.core.subcategory_app.schemas.subcategory_dto import SubCategoryAllData


class CreateCategory(BaseModel):
    name_category: Annotated[str, Field(max_length=150)]
    icon_category: Annotated[str, Field()]


class CategoryBase(CreateCategory):
    """
    Базовый DTO для категорий
    """

    id_category: Annotated[int, Field()]
    subcategory: Annotated[List[SubCategoryAllData], Field()]


class CategoryIsCreated(BaseModel):

    is_created: bool


class CategoryIsFinded(BaseModel):

    is_find: bool


class DataCategoryToUpdate(BaseModel):

    name_category: str
    new_name_category: str


class CategoryIsUpdated(BaseModel):

    is_updated: bool


class CategoriesList(BaseModel):
    categories: Annotated[List[CategoryBase], Field()]
