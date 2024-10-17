# System
from typing import Dict

# Other
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Local
from src.database.mainbase import MainBase


class Favourite(MainBase):
    # Таблица Избранное

    # Связи
    id_user: Mapped[int] = mapped_column(
        ForeignKey("User.id"), type_=Integer
    )  # id пользователя

    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id"), type_=Integer
    )  # id продукта

    fav_user: Mapped["User"] = relationship(
        "User", back_populates="favourites_user", uselist=False
    )

    product_info: Mapped["Product"] = relationship(
        "Product", back_populates="product_info_for_fav", uselist=False
    )

    def read_model(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __str__(self) -> str:
        # Возвращает строковый объект класса
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        # Возвращает строковый объект класса
        return self.__str__()
