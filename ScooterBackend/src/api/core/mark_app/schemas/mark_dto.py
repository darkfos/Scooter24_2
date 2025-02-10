from pydantic import BaseModel, Field
from typing import Annotated, List


class MarkBase(BaseModel):

    id_mark: Annotated[int, Field()]
    name_mark: Annotated[str, Field()]


class ProductMarks(BaseModel):
    id_mark: Annotated[int, Field()]
    id_product: Annotated[int, Field()]


class AllMarks(BaseModel):
    marks: Annotated[List[MarkBase], Field()]
