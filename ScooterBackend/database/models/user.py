#System
import datetime
from typing import List, Dict

#Other
from sqlalchemy import Integer, Text, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column

#Local
from ScooterBackend.database.mainbase import MainBase


class User(MainBase):
    #Таблица пользователь

    #Почта пользователя
    email_user: Mapped[str] = mapped_column(type_=Text, nullable=False, unique=True, index=True)

    #Пароль пользователя
    password_user: Mapped[str] = mapped_column(type_=String(60), nullable=False)

    #Ключ обновление пароля пользователя
    secret_update_key: Mapped[str] = mapped_column(type_=String(80), nullable=True, default="")

    #Опциональные данные
    name_user: Mapped[str] = mapped_column(type_=String(100), nullable=True) #Имя пользователя
    surname_user: Mapped[str] = mapped_column(type_=String(150), nullable=True)

    #Отображаемое имя пользователя
    main_name_user: Mapped[str] = mapped_column(type_=String(250), nullable=False)

    #Дата регистрации
    date_registration: Mapped[datetime.date] = mapped_column(type_=Date, nullable=False, default=datetime.date)

    #Дата обновления информации
    date_update: Mapped[datetime.date] = mapped_column(type_=Date, nullable=False, default=datetime.date)

    ###Связи c таблицами###

    #Избранное
    favourites_user: Mapped[List["Favourite"]] = relationship(
        "Favourite", back_populates="fav_user", uselist=True)
    #Заказы
    orders_user: Mapped[List["Order"]] = relationship("Order", back_populates="ord_user", uselist=True) #Заказы
    #История покупок
    history_buy_user: Mapped[List["HistoryBuy"]] = relationship(
        "HistoryBuy", back_populates="hst_user", uselist=True)
    #Отзывы
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user", uselist=True)

    def read_model(self) -> Dict[str, str]:
        return {
            k: v
            for k, v in self.__dict__.items()
            if k != "_sa_instance_state"
        }

    def __str__(self) -> str:
        #Возвращает строковый объект класса
        return str(
            {
                k: v
                for k, v in self.__dict__.items()
            }
        )

    def __repr__(self):
        #Возвращает строковый объект класса
        return self.__str__()
