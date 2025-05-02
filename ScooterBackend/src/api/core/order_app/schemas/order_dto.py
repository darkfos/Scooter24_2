# Other libraries
import datetime

from pydantic import BaseModel, Field
from typing import Union, Annotated, List, Dict, Any

# Local
...


class OrderBase(BaseModel):
    product_data: Annotated[
        List[
            Dict[
                str,
                Union[
                    str,
                    int,
                    float,
                    datetime.date,
                    None,
                    list[Dict[str, Union[int, str]]],
                ],
            ]
        ],
        Field(),
    ]


class AddOrder(BaseModel):

    id_products: Annotated[List[int], Field()]
    date_create: datetime.date = datetime.date.today()


class ProductOrder(BaseModel):
    id_product: Annotated[int, Field()]
    quantity: Annotated[int, Field()]
    price: Annotated[int, Field()]


class BuyOrder(BaseModel):
    id_orders: Annotated[List[int], Field()]
    products: Annotated[List[ProductOrder], Field()]
    username: Annotated[str, Field()] = None
    email: Annotated[str, Field()] = None
    telephone: Annotated[str, Field()] = None
    address: Annotated[str, Field()] = None
    type_delivery: Annotated[str, Field()] = None
    price_delivery: Annotated[float, Field()] = None
    date_create: datetime.date = datetime.date.today()


class OrderAndUserInformation(OrderBase):
    order_data: Any


class ListOrderAndUserInformation(BaseModel):

    orders: List[OrderAndUserInformation]
