# Other libraries
from pydantic import BaseModel, Field
from typing import Union, Annotated, Dict

# Local
...


class HistoryBuyBase(BaseModel):

    id_product: Annotated[int, Field(gt=-1)]


class HistoryAndUserInformation(HistoryBuyBase):

    user_data: Annotated[Dict[str, Union[str, int]], Field()]
    product_data: Annotated[Dict[str, Union[str, int]], Field()]
