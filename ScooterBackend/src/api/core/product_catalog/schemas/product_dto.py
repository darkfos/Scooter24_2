# System
import datetime
from typing import List, Union, Annotated

# Other libraries
from pydantic import BaseModel, Field

# Local
...


class ProductBase(BaseModel):

    article_product: Annotated[str, Field(max_length=300)]
    title_product: Annotated[str, Field(max_length=500)]
    brand: Annotated[str, Field(max_length=150)]
    weight_product: Annotated[float, Field(ge=0)]
    id_category: Annotated[Union[None, int], Field(default=None)]
    id_subcategory_thirst_level: Annotated[Union[None, int], Field(default=None)]
    id_subcategory_second_level: Annotated[Union[None, int], Field(default=None)]
    explanation_product: Annotated[str, Field()]
    brand_mark: Annotated[str, Field(max_length=150)]
    model: Annotated[str, Field(max_length=300)]
    photo_product: Annotated[str, Field()] = None
    quantity_product: Annotated[int, Field(gt=-1)]
    price_product: Annotated[float, Field(gt=-1)]
    price_with_discount: Annotated[float, Field()]
    date_create_product: Annotated[datetime.date, Field(default=datetime.date.today())]
    date_update_information: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ]
    product_discount: Annotated[int, Field(lt=100)]


class ListProductBase(BaseModel):

    products: Annotated[List[ProductBase], Field()]


class ProductAllInformation(ProductBase):

    reviews: List[dict]
    orders: List[dict]
    favourites: List[dict]
    categories: List[dict]


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

    is_created: bool
    product_name: str


class UpdateProductDiscount(BaseModel):

    product_discount: Annotated[int, Field(lt=100)]
    date_update_information: Annotated[
        datetime.date, Field(default=datetime.date.today())
    ]
