#Other
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import List

#Local
from ScooterBackend.database.mainbase import MainBase


class Category(MainBase):
    #Таблица категории товаров

    #Колонки таблицы
    name_category: Mapped[str] = mapped_column(type_=String(250), nullable=False) #Название категории

    #Связи с таблицами
    product: Mapped[List["Product"]] = relationship("Product", back_populates="category")

    def __str__(self):
        #Возвращает строковый объект класса
        return str(
            {
                k: v
                for k, v in self.__dict__.items()
            }
        )

    def __repr__(self) -> str:
        #Возвращает строковый объект класса
        return self.__str__()