#System
import datetime
from typing import List, Union, Annotated

#Other libraries
from pydantic import BaseModel, Field
from sqlalchemy import LargeBinary
from fastapi import UploadFile
from fastapi.responses import FileResponse

#Local
from ScooterBackend.database.models.category import Category


class ProductBase(BaseModel):

    title_product: Annotated[str, Field(max_length=500)]
    price_product: Annotated[float, Field(gt=-1)]
    quantity_product: Annotated[int, Field(gt=-1)]
    explanation_product: Annotated[str, Field(max_length=780)]
    article_product: Annotated[str, Field(max_length=300)]
    tags: Annotated[str, Field(min_length=0)]
    other_data: Annotated[str, Field(min_length=0)]
    id_category: int
    photo_product: Annotated[str, Field()] = None
    date_create_product: Annotated[datetime.date, Field(default=datetime.date.today())]
    date_update_information: Annotated[datetime.date, Field(default=datetime.date.today())]


class ProductAllInformation(ProductBase):

    reviews: List[dict]
    category_data: List[dict]
    orders: List[dict]
    favourites: List[dict]


class DeleteProduct(BaseModel):

    id_product: int


class UpdateProduct(BaseModel):

    title_product: Annotated[str, Field(max_length=200, default=None)] = None
    price_product: Annotated[float, Field(default=None)] = None
    quantity_product: Annotated[int, Field(gt=-1, default=None)] = None
    explanation_product: Annotated[str, Field(default=None)] = None
    article_product: Annotated[str, Field(max_length=150, default=None)] = None
    tags: Annotated[str, Field(min_length=0, default=None)] = None
    other_data: Annotated[str, Field(min_length=0, default=None)] = None
    date_update_information: Annotated[datetime.date, Field(default=datetime.date.today())]


class ProductIsCreated(BaseModel):

    is_created: bool
    product_name: str