from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Double
from typing import Dict
from src.database.mainbase import MainBase


class OrderProducts(MainBase):

    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id", ondelete="CASCADE"), type_=Integer
    )
    id_order: Mapped[int] = mapped_column(
        ForeignKey("Order.id", ondelete="CASCADE"), type_=Integer
    )
    count_product: Mapped[int] = mapped_column(type_=Integer, nullable=True)
    price: Mapped[float] = mapped_column(type_=Double, nullable=True)

    product_data: Mapped["Product"] = relationship(
        "Product", back_populates="orders_list", uselist=False
    )
    order_data: Mapped["Order"] = relationship(
        "Order", back_populates="product_list", uselist=False
    )

    def read_model(self) -> Dict[str, str]:
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }

    def __str__(self) -> str:
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        return self.__str__()
