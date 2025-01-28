from pydantic import BaseModel, Field
from typing import Annotated, List, Union


class BrandBase(BaseModel):

    name_brand: Annotated[str, Field()]


class AllBrands(BaseModel):

    brands: Annotated[Union[List, List[BrandBase]], Field()]
