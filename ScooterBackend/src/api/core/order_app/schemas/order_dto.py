# Other libraries
import datetime

from pydantic import BaseModel, Field
from typing import Union, Annotated, List, Dict

# Local
...


class OrderBase(BaseModel):

    product_data: Annotated[
        Dict[str, Union[str, int, datetime.date, None, dict]], Field()
    ]


class AddOrder(BaseModel):

    id_product: int
    date_create: datetime.date = datetime.date.today()


class OrderAndUserInformation(OrderBase):
    order_data: Annotated[
        Dict[Union[str, int], Union[str, int, datetime.date]], Field()
    ]


class ListOrderAndUserInformation(BaseModel):

    orders: List[OrderAndUserInformation]
