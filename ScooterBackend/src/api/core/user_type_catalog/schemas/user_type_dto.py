from pydantic import BaseModel, Field
from typing import Annotated, List

class UserTypeBase(BaseModel):
    id: Annotated[int, Field()]
    name_type: Annotated[str, Field(max_length=100)]

class NewUserType(BaseModel):
    name_type: Annotated[str, Field(max_length=100)]

class AllUserType(BaseModel):
    user_types: Annotated[List[UserTypeBase], Field()]