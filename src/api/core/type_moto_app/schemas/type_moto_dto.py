from pydantic import BaseModel, Field
from typing import Annotated, Union, List


class TypeModelBase(BaseModel):
    id_mt: Annotated[int, Field()]
    name_type: Annotated[Union[str, None], Field(default=None)]


class ProductTypeModels(BaseModel):
    id_product: Annotated[int, Field()]
    id_moto_type: Annotated[int, Field()]


class ListTypeModelBase(BaseModel):
    moto_types: Annotated[Union[List, List[TypeModelBase]], Field()]
