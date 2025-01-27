from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Local
from src.database.mainbase import MainBase


class TypeMoto(MainBase):

    # Название типа транспорта
    name_moto_type: Mapped[str] = mapped_column(
        type_=String(length=125), nullable=False, unique=True
    )

    # Данные продуктов
    product_data: Mapped[List["Product"]] = relationship(
        "Product", back_populates="type_moto_data", uselist=True
    )

    def read_model(self) -> dict:
        return {
            i: self.__dict__[i]
            for i in self.__dict__.keys()
            if not i.startswith("_")
        }

    def __str__(self) -> str:
        return str({i: self.__dict__[i] for i in self.__dict__.keys()})

    def __repr__(self) -> str:
        return self.__str__()
