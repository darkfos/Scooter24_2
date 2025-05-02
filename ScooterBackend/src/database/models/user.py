# System
from datetime import date
from typing import List, Dict

# Other
from sqlalchemy import (
    Integer,
    Text,
    String,
    ForeignKey,
    Date,
    Boolean,
    LargeBinary,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Local
from src.database.mainbase import MainBase


class User(MainBase):
    # Таблица пользователь

    # Тип пользователя
    id_type_user: Mapped[int] = mapped_column(
        ForeignKey("Usertype.id"), type_=Integer, nullable=False
    )

    # Активированный аккаунт
    is_active: Mapped[bool] = mapped_column(
        type_=Boolean, nullable=False, default=False
    )

    # Почта пользователя
    email_user: Mapped[str] = mapped_column(
        type_=Text, nullable=False, unique=True, index=True
    )

    # Пароль пользователя
    password_user: Mapped[str] = mapped_column(
        type_=LargeBinary, nullable=False
    )

    # Ключ обновление пароля пользователя
    secret_update_key: Mapped[str] = mapped_column(
        type_=String(80), nullable=True, default=""
    )

    # Ключ для регистрации пользователя
    secret_create_key: Mapped[str] = mapped_column(
        type_=String(80), nullable=True, default=""
    )

    # Опциональные данные
    name_user: Mapped[str] = mapped_column(type_=String(100), nullable=True)

    # Отображаемое имя пользователя
    main_name_user: Mapped[str] = mapped_column(
        type_=String(250), nullable=True
    )

    # Дата регистрации
    date_registration: Mapped[date] = mapped_column(
        type_=Date, nullable=False, default=date.today()
    )

    # Дата обновления информации
    date_update: Mapped[date] = mapped_column(
        type_=Date, nullable=False, default=date.today()
    )

    # Дата рождения
    date_birthday: Mapped[date] = mapped_column(
        type_=Date, nullable=True, default=date.today()
    )

    # Город пользователя
    address_city: Mapped[str] = mapped_column(type_=String(length=250), nullable=True)

    # Адресные данные
    address: Mapped[str] = mapped_column(type_=Text, nullable=True)

    # Телефон
    telephone: Mapped[str] = mapped_column(
        type_=String(length=65), nullable=True
    )

    # Связи c таблицами

    # Избранное
    favourites_user: Mapped[List["Favourite"]] = relationship(
        "Favourite", back_populates="fav_user", uselist=True
    )

    # Заказы
    orders_user: Mapped[List["Order"]] = relationship(
        "Order", back_populates="ord_user", uselist=True
    )

    # Отзывы
    reviews: Mapped[List["Review"]] = relationship(
        "Review", back_populates="user", uselist=True
    )

    # Тип пользователя
    type_user_data: Mapped["UserType"] = relationship(
        "UserType", back_populates="user_data", uselist=False
    )

    # Данные гаража
    garage_data: Mapped[List["Garage"]] = relationship(
        "Garage", back_populates="user_data", uselist=True
    )

    def read_model(self) -> Dict[str, str]:
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }

    def __str__(self) -> str:
        # Возвращает строковый объект класса
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self):
        # Возвращает строковый объект класса
        return self.__str__()
