from pydantic import BaseModel, Field
from typing import Annotated, Union, List, Dict


class GarageBase(BaseModel):

    id_garage: Annotated[int, Field()]
    id_model: Annotated[int, Field()]
    id_mark: Annotated[int, Field()]
    id_user: Annotated[int, Field()]
    id_moto_type: Annotated[int, Field()]

    # Данные
    models_data: Annotated[Dict, Field()]
    mark_data: Annotated[Dict, Field()]
    moto_type_data: Annotated[Dict, Field()]


class ListGarageBase(BaseModel):
    garage: Annotated[Union[List, List[GarageBase]], Field()]


class AddNewMotoToGarage(BaseModel):

    id_model: Annotated[int, Field()]
    id_mark: Annotated[int, Field()]
    id_moto_type: Annotated[int, Field()]
