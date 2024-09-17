# System
from typing import Annotated
import datetime

# Other libraries
from pydantic import BaseModel, Field, EmailStr


class AdminBase(BaseModel):

    email_admin: Annotated[EmailStr, Field(max_length=150)]
    password_user: Annotated[str, Field()]
    date_create: Annotated[datetime.date, Field(default=datetime.date.today())]
    date_update: Annotated[datetime.date, Field(default=datetime.date.today())]


class AdminIsCreated(BaseModel):

    is_created: bool
