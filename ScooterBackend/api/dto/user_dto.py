#Other libraries
import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Union, List, Dict

#Local
from database.models.order import Order
from database.models.review import Review
from database.models.history_buy import HistoryBuy
from database.models.favourite import Favourite


class UserBase(BaseModel):
    """
    Начальный объект пользователя
    """

    email_user: Annotated[EmailStr, Field(EmailStr())]
    password_user: Annotated[str, Field(min_length=6, max_length=60)]
    name_user: Annotated[str, Field(max_length=100)]
    surname_user: Annotated[str, Field(max_length=150)]
    main_name_user: Annotated[str, Field(max_length=250)]


class InformationAboutUser(BaseModel):
    """
    Информация о пользователе кроме пароля
    """

    email_user: Annotated[EmailStr, Field(EmailStr())]
    name_user: Annotated[str, Field(max_length=100)]
    surname_user: Annotated[str, Field(max_length=150)]
    main_name_user: Annotated[str, Field(max_length=250)]
    date_registration: Annotated[datetime.date, Field(default=datetime.date.today())]


class AddUser(UserBase):
    """
    Добавление нового пользователя
    """

    date_registration: datetime.date = datetime.date.today()


class UpdateDataUser(BaseModel):
    """
     Обновление данных о пользователе
    """

    name_user: Annotated[str, Field(le=100)]
    surname_user: Annotated[str, Field(le=150)]
    main_name_user: Annotated[str, Field(le=250)]
    date_update: Annotated[datetime.date, Field(default=datetime.date.today())]


class UserReviewData(InformationAboutUser):
    """
    Информация о пользователе + все его отзывы
    """

    reviews: List[Dict]


class UserFavouritesData(InformationAboutUser):
    """
    Информация о пользователе + все его товары в избранном
    """

    favourites: List[Dict]


class UserOrdersData(InformationAboutUser):
    """
    Информация о пользователе + все его заказы
    """

    orders: List[Dict]


class UserHistoryData(InformationAboutUser):
    """
    Информация о пользователе + вся история заказов
    """

    history: List[Dict]


class UserIsUpdated(BaseModel):
    """
    Обновление данных пользователя
    """

    is_updated: bool


class DataToUpdate(BaseModel):
    """
    Информация о пользователе кроме пароля для обновления
    """

    email_user: Annotated[EmailStr, Field(EmailStr())] = None
    name_user: Annotated[str, Field(max_length=100)] = None
    surname_user: Annotated[str, Field(max_length=150)] = None
    main_name_user: Annotated[str, Field(max_length=250)] = None
    date_update: Annotated[datetime.date, Field(default=datetime.date.today())]


class DataToUpdateUserPassword(BaseModel):
    """
    Обновление пароля пользователя
    """

    user_old_password: Annotated[str, Field(min_length=6, max_length=60)]
    new_password: Annotated[str, Field(min_length=6, max_length=60)]
    date_update: Annotated[datetime.date, Field(default=datetime.date.today())]


class UserIsDeleted(BaseModel):
    """
    Удаление пользователя
    """

    is_deleted: bool


class UpdateAddressDate(BaseModel):
    """
    Обновление адресных данных пользователя
    """

    name_user_address: Annotated[str, Field(max_length=200)]
    surname_user_address: Annotated[str, Field(max_length=200)]
    name_company_address: Annotated[str, Field(max_length=200)]
    country_address: Annotated[str, Field(max_length=250)]
    address_street: Annotated[str, Field(max_length=450)]
    address_rl_et_home: Annotated[str, Field(max_length=250)]
    address_locality: Annotated[str, Field(max_length=300)]
    address_area: Annotated[str, Field(max_length=350)]
    address_index: Annotated[int, Field()]
    address_phone_number: Annotated[str, Field(max_length=40)]


class AllDataUser(InformationAboutUser):
    """
    Полная информация о пользователе
    """

    orders: Union[List, List[Dict]]
    favourite: Union[List, List[Dict]]
    history: Union[List, List[Dict]]
    reviews: Union[List, List[Dict]]

    address: UpdateAddressDate