#System
import datetime
from typing import List, Dict

#Other
from sqlalchemy import Integer, Text, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column

#Local
from database.mainbase import MainBase


class Order(MainBase):
    #Таблица заказы

    #Дата заказа
    date_buy: Mapped[datetime.date] = mapped_column(type_=Date, unique=False, nullable=False, default=datetime.date)

    #Связи
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id"), type_=Integer) #id пользователя
    id_product: Mapped[int] = mapped_column(ForeignKey("Product.id"), type_=Integer) #id продукта

    ord_user: Mapped["User"] = relationship("User", back_populates="orders_user", uselist=False) #Инф. об пользователе
    product_info: Mapped["Product"] = relationship("Product", back_populates="order", uselist=False) #Инф. об продукте

    def read_model(self) -> Dict[str, str]:
        return {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        }

    def __str__(self) -> str:
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