from pydantic import BaseModel, Field
from typing import Annotated, List, Union


class BrandBase(BaseModel):

    id_brand: Annotated[int, Field()]
    name_brand: Annotated[str, Field()]
    url_brand: Annotated[Union[str, None], Field()]


class AllBrands(BaseModel):

    brands: Annotated[Union[List, List[BrandBase]], Field()]
