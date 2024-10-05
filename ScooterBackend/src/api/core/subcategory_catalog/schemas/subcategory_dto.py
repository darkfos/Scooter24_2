from pydantic import BaseModel, Field
from typing import Annotated, List, Dict


class SubCategoryBase(BaseModel):

    name: Annotated[str, Field(max_length=225)]
    id_category: Annotated[int, Field()]


class AllSubCategories(BaseModel):

    all_subcategory: Annotated[List[SubCategoryBase], Field()]