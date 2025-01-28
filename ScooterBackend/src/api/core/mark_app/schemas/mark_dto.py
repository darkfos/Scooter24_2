from pydantic import BaseModel, Field
from typing import Annotated, List


class MarkBase(BaseModel):

    name_mark: Annotated[str, Field()]


class AllMarks(BaseModel):
    marks: Annotated[List[MarkBase], Field()]
