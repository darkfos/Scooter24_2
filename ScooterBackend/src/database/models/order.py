# System
from typing import Dict

# Other
from sqlalchemy import Integer, ForeignKey, Date, Enum, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Local
from src.database.mainbase import MainBase
from datetime import date
from src.database.models.enums.order_enum import OrderTypeOperationsEnum


class Order(MainBase):
    # Таблица заказы

    # Дата заказа
    date_buy: Mapped[date] = mapped_column(
        type_=Date, unique=False, nullable=False, default=date.today()
    )

    # Тип операции
    type_operation: Mapped[str] = mapped_column(
        type_=Enum(OrderTypeOperationsEnum),
        unique=False,
        nullable=False,
        default=OrderTypeOperationsEnum.NO_BUY.value,
    )

    # Количество товаров
    count_product: Mapped[int] = mapped_column(
        type_=Integer, unique=False, nullable=False, default=1
    )

    price_result: Mapped[float] = mapped_column(
        type_=Numeric, unique=False, nullable=False
    )

    # Связи
    id_user: Mapped[int] = mapped_column(
        ForeignKey("User.id"), type_=Integer
    )  # id пользователя
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id"), type_=Integer
    )  # id продукта

    ord_user: Mapped["User"] = relationship(
        "User", back_populates="orders_user", uselist=False
    )  # Инф. об пользователе
    product_info: Mapped["Product"] = relationship(
        "Product", back_populates="order", uselist=False
    )  # Инф. об продукте

    def read_model(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __str__(self) -> str:
        # Возвращает строковый объект класса
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        # Возвращает строковый объект класса
        return self.__str__()
