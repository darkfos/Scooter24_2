from pydantic import BaseModel, Field
from typing import Annotated, Union, List


class TypeModelBase(BaseModel):
    id_mt: Annotated[int, Field()]
    name_type: Annotated[Union[str, None], Field(default=None)]


class ListTypeModelBase(BaseModel):
    moto_types: Annotated[Union[List, List[TypeModelBase]], Field()]
