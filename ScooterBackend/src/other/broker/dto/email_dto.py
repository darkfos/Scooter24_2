from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from typing import Annotated


class TypeEmailSendMessage(Enum):

    CREATE: str = "регистрация"
    UPDATE: str = "обновление"


class EmailData(BaseModel):
    email: Annotated[EmailStr, Field(min_length=1)]
    secret_key: Annotated[str, Field(min_length=6, max_length=6)]


class EmailQueueMessage(BaseModel):
    email_data: EmailData
    type: Annotated[TypeEmailSendMessage, Field()]