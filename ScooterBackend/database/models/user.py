#Other
from sqlalchemy import Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

#Local
from ScooterBackend.database.mainbase import MainBase


class User(MainBase):
    #Таблица пользователь

    #Почта пользователя
    email_user: Mapped[str] = mapped_column(type_=Text, nullable=False)

    #Пароль пользователя
    password_user: Mapped[str] = mapped_column(type_=String(250), nullable=False)

    #Опциональные данные
    name_user: Mapped[str] = mapped_column(type_=String(300), nullable=True) #Имя пользователя
    surname_user: Mapped[str] = mapped_column(type_=String(300), nullable=True)

    #Отображаемое имя пользователя
    main_name_user: Mapped[str] = mapped_column(type_=String(400), nullable=False)

    ###Связи c таблицами###

    #Избранное
    favourites_user: Mapped[List["Favourite"]] = relationship("Favourite", back_populates="fav_user")
    #Заказы
    orders_user: Mapped[List["Order"]] = relationship("Order", back_populates="ord_user") #Заказы
    #История покупок
    history_buy_user: Mapped[List["HistoryBuy"]] = relationship("HistoryBuy", back_populates="hst_user")
    #Отзывы
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user")

    def __str__(self) -> str:
        #Возвращает строковый объект класса
        return str(
            dict(
                k=v
                for k, v in self.__dict__.items()
            )
        )

    def __repr__(self):
        #Возвращает строковый объект класса
        return self.__str__()