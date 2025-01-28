from pydantic import BaseModel, Field
from typing import Annotated, List


class MarkBase(BaseModel):

    id_mark: Annotated[int, Field()]
    name_mark: Annotated[str, Field()]


class AllMarks(BaseModel):
    marks: Annotated[List[MarkBase], Field()]
