# Other libraries
import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from sqlalchemy import Row

from typing import Union, Annotated, List, Dict, Any, Optional


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
    order_data: Annotated[
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
    type_buy: Annotated[str, Field()] = None
    price_delivery: Annotated[float, Field()] = None
    date_create: datetime.date = datetime.date.today()


class OrderAndUserInformation(OrderBase):
    order_data: Dict
    product_data: List[Dict]


class ListOrderAndUserInformation(BaseModel):

    orders: List[OrderAndUserInformation]

class OrderProductsSchema(BaseModel):
    id: int = Field(gt=0)
    id_product: int = Field(gt=0)
    id_order: int = Field(gt=0)
    count_product: int = Field(gt=0)
    price: float = Field(gt=0)

    class Config:
        model_config = {"from_attributes": True}
        from_attributes = True
        extra = 'ignore'


class OrderSchema(BaseModel):
    date_buy: datetime.datetime
    type_operation: str
    type_buy: str
    email_user: Optional[str] = None
    transaction_id: Optional[str] = None
    user_name: Optional[str] = None
    telephone_number: Optional[str] = None
    label_order: Optional[UUID] = None
    address: Optional[str] = None
    delivery_method: Optional[str] = None
    price_result: float
    id_user: Optional[int] = None

    class Config:
        model_config = {"from_attributes": True}
        from_attributes = True
        extra = 'ignore'


class OrderIsBuy(BaseModel):
    is_buy: Annotated[bool, Field(default=False)]