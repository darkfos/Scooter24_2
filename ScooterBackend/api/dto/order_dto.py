#Other libraries
from pydantic import BaseModel, Field
from typing import Union, Annotated, List, Dict

#Local
...


class OrderBase(BaseModel):

    product_data: Annotated[Dict[str, Union[str, int]], Field()]


class AddOrder(BaseModel):

    id_product: int


class OrderAndUserInformation(OrderBase):

    user_data: Annotated[Dict[str, Union[str, int]], Field()]