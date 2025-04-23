from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class EmailData(BaseModel):
    email: Annotated[EmailStr, Field(min_length=1)]
    secret_key: Annotated[str, Field(min_length=6, max_length=6)]
