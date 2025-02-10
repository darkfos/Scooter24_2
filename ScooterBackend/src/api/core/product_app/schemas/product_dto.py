# System
import datetime
from typing import List, Annotated, Union

from fastapi import UploadFile

# Other libraries
from pydantic import BaseModel, Field

from src.api.core.photo_app.dto.photo_dto import PhotoBase
from src.api.core.subcategory_app.schemas.subcategory_dto import (
    SubCategoryBase,
)
from src.api.core.mark_app.schemas.mark_dto import ProductMarks
from src.api.core.type_moto_app.schemas.type_moto_dto import ProductTypeModels


class ProductBase(BaseModel):

    id_product: Annotated[Union[int, None], Field()]
    label_product: Annotated[str, None, Field()]
    type_pr: Annotated[List[ProductTypeModels], Field()]
    article_product: Annotated[str, Field(max_length=300)]
    title_product: Annotated[str, Field(max_length=500)]
    brand: int
    brand_mark: Annotated[List[ProductMarks], Field()]
    models: Union[List, None] = None
    id_sub_category: Annotated[Union[int, None], Field(default=None)]
    weight_product: Annotated[float, Field(ge=0)]
    is_recommended: Annotated[Union[bool, None], Field()]
    explanation_product: Annotated[str, Field()]
    quantity_product: Annotated[int, Field(gt=-1)]
    price_product: Annotated[float, Field(gt=-1)]
    date_create_product: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ]
    date_update_information: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ]
    product_discount: Annotated[int, Field(lt=100)]
    photo: Annotated[
        List[PhotoBase], Field(default=None)
    ] = None

    @classmethod
    def change_product_discount(cls) -> None:
        cls.product_discount = (
            cls.price_product - cls.price_with_discount
        ) // cls.price_product


class ListProductBase(BaseModel):

    products: Annotated[List[ProductBase], Field()]


class ProductAllInformation(ProductBase):

    reviews: Annotated[List[dict], Field()]
    orders: Annotated[List[dict], Field]
    favourites: Annotated[List[dict], Field()]
    categories: Annotated[SubCategoryBase, Field()]


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
    date_update_information: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ]


class ProductIsCreated(BaseModel):

    is_created: Annotated[bool, Field()]
    product_name: Annotated[Union[str, int], Field()]


class UpdateProductDiscount(BaseModel):

    product_discount: Annotated[int, Field(lt=100)]
    date_update_information: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ]
