#System
from typing import Annotated, List

#Other libraries
from pydantic import BaseModel, Field


class TypeWorkerBase(BaseModel):

    name_type: Annotated[str, Field(max_length=300)]

class TypeWorkerList(BaseModel):
    type_worker: Annotated[List[TypeWorkerBase], Field()]