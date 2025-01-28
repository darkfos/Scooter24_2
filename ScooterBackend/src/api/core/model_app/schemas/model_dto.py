from pydantic import BaseModel, Field
from typing import List, Annotated


class ModelBase(BaseModel):

    name_model: Annotated[str, Field(max_length=100)]


class AllModelBase(BaseModel):

    all_models: Annotated[List[ModelBase], Field()]
