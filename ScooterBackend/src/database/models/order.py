from typing import Dict, List


from sqlalchemy import (
    Integer,
    ForeignKey,
    Enum,
    Numeric,
    UUID,
    Text,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database.mainbase import MainBase
from datetime import datetime
from src.database.models.enums.order_enum import OrderTypeOperationsEnum
from src.database.models.enums.delivery_type_enum import DeliveryMethod
from src.database.models.enums.type_buy_enum import TypeBuy


class Order(MainBase):
    date_buy: Mapped[datetime] = mapped_column(
        type_=DateTime, unique=False, nullable=False, default=datetime.now()
    )

    type_operation: Mapped[str] = mapped_column(
        type_=Enum(OrderTypeOperationsEnum),
        unique=False,
        nullable=False,
        default=OrderTypeOperationsEnum.NO_BUY.value,
    )

    type_buy: Mapped[str] = mapped_column(
        type_=Enum(TypeBuy), unique=False, nullable=True
    )

    email_user: Mapped[str] = mapped_column(
        type_=Text, unique=False, nullable=True
    )

    transaction_id: Mapped[str] = mapped_column(
        type_=Text, unique=False, nullable=True
    )

    user_name: Mapped[str] = mapped_column(
        type_=String(length=100), unique=False, nullable=True
    )

    telephone_number: Mapped[str] = mapped_column(
        type_=String(length=65), unique=False, nullable=True
    )

    label_order: Mapped[str] = mapped_column(
        type_=UUID, unique=True, nullable=True
    )

    address: Mapped[str] = mapped_column(
        type_=Text, unique=False, nullable=True
    )

    delivery_method: Mapped[str] = mapped_column(
        type_=Enum(DeliveryMethod), unique=False, nullable=True
    )

    price_result: Mapped[float] = mapped_column(
        type_=Numeric, unique=False, nullable=False
    )

    id_user: Mapped[int] = mapped_column(
        ForeignKey("User.id", ondelete="SET NULL"),
        type_=Integer,
        nullable=True,
    )
    ord_user: Mapped["User"] = relationship(
        "User", back_populates="orders_user", uselist=False
    )
    product_list: Mapped[List["OrderProducts"]] = relationship(
        "OrderProducts",
        back_populates="order_data",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def read_model_orm(self) -> Dict[str, str]:
        result_dict = {"product_list": [], "ord_user": []}

        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                if k == "product_list" or k == "ord_user":
                    for data in self.__dict__[k]:
                        result_dict[k].append(data.read_model())
                else:
                    result_dict[k] = v

        return result_dict

    def read_model(self) -> Dict[str, str]:
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }

    def __str__(self) -> str:
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        return self.__str__()
