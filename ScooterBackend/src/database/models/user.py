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

    id_type_user: Mapped[int] = mapped_column(
        ForeignKey("Usertype.id"), type_=Integer, nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        type_=Boolean, nullable=False, default=False
    )

    email_user: Mapped[str] = mapped_column(
        type_=Text, nullable=False, unique=True, index=True
    )

    password_user: Mapped[str] = mapped_column(
        type_=LargeBinary, nullable=False
    )

    secret_update_key: Mapped[str] = mapped_column(
        type_=String(80), nullable=True, default=""
    )

    secret_create_key: Mapped[str] = mapped_column(
        type_=String(80), nullable=True, default=""
    )

    name_user: Mapped[str] = mapped_column(type_=String(100), nullable=True)

    main_name_user: Mapped[str] = mapped_column(
        type_=String(250), nullable=True
    )

    date_registration: Mapped[date] = mapped_column(
        type_=Date, nullable=False, default=date.today()
    )

    date_update: Mapped[date] = mapped_column(
        type_=Date, nullable=False, default=date.today()
    )

    date_birthday: Mapped[date] = mapped_column(
        type_=Date, nullable=True, default=date.today()
    )

    address_city: Mapped[str] = mapped_column(
        type_=String(length=250), nullable=True
    )

    address: Mapped[str] = mapped_column(type_=Text, nullable=True)

    telephone: Mapped[str] = mapped_column(
        type_=String(length=65), nullable=True
    )

    favourites_user: Mapped[List["Favourite"]] = relationship(
        "Favourite",
        back_populates="fav_user",
        uselist=True,
        cascade="all, delete-orphan",
    )

    orders_user: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="ord_user",
        uselist=True,
        cascade="save-update",
        passive_deletes=True,
    )

    reviews: Mapped[List["Review"]] = relationship(
        "Review",
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )

    type_user_data: Mapped["UserType"] = relationship(
        "UserType", back_populates="user_data", uselist=False
    )

    garage_data: Mapped[List["Garage"]] = relationship(
        "Garage",
        back_populates="user_data",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def read_model(self) -> Dict[str, str]:
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }

    def __str__(self) -> str:
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self):
        return self.__str__()
