#Other
from sqlalchemy import Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

#Local
from ScooterBackend.database.mainbase import MainBase


class Order(MainBase):
    #Таблица заказы

    #Связи
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id"), type_=Integer) #id пользователя
    id_product: Mapped[int] = mapped_column(ForeignKey("Product.id"), type_=Integer) #id продукта

    ord_user: Mapped["User"] = relationship("User", back_populates="orders_user") #Инф. об пользователе
    product_info: Mapped["Product"] = relationship("Product", back_populates="order") #Инф. об продукте

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