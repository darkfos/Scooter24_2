#System
from typing import Annotated

#Other libraries
from pydantic import BaseModel, Field


class TypeWorkerBase(BaseModel):

    name_type: Annotated[str, Field(max_length=300)]