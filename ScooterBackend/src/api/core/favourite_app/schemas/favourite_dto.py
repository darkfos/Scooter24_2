# Other libraries
from pydantic import BaseModel, Field
from typing import Annotated, Union, List, Dict

# Local


class FavouriteBase(BaseModel):

    product_info: Annotated[Dict[str, Union[str, int, List]], Field()]


class ListFavouriteBase(BaseModel):

    favourites: Annotated[List[FavouriteBase], Field()]


class DeleteFavourite(BaseModel):

    id_favourite: Annotated[int, Field()]


class AddFavourite(BaseModel):

    id_product: int


class FavouriteInformation(FavouriteBase):

    user_detail_information: Annotated[Dict[str, Union[str, int]], Field()]


class FavouriteSmallData(BaseModel):

    id_fav: int
    id_product: int
    id_user: int
