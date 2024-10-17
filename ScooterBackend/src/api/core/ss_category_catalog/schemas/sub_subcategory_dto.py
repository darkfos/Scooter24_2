from pydantic import BaseModel, Field
from typing import Annotated, List


class SubSubCategoryBase(BaseModel):
    name: Annotated[str, Field(max_length=225)]
    id_sub_category: Annotated[int, Field()]


class AllSubSubCategory(BaseModel):
    all_sub_subcategories: Annotated[List[SubSubCategoryBase], Field()]
