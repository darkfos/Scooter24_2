from pydantic import BaseModel, Field
from typing import List, Annotated


class ProductModelsBase(BaseModel):
    id_product: Annotated[int, Field()]
    id_model: Annotated[int, Field()]


class AllProductModels(BaseModel):
    all_models: Annotated[List[ProductModelsBase], Field()]
