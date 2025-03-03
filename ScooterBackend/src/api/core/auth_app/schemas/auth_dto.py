from pydantic import BaseModel, Field, EmailStr


class CreateToken(BaseModel):

    email: EmailStr = Field()
    password: str = Field(min_length=6, max_length=60)


class Tokens(BaseModel):

    token: str = Field()
    refresh_token: str = Field()
    token_type: str = "bearer"


class RegistrationUser(BaseModel):

    is_registry: bool = Field(default=False)


class RefreshUpdateToken(BaseModel):

    refresh_token: str = Field()


class AccessToken(BaseModel):

    access_token: str = Field()
    token_type: str = "bearer"
    refresh_token: str = Field()


class UpdateUserPassword(BaseModel):

    old_password: str = Field()
    new_password: str = Field(max_length=60, min_length=6)
