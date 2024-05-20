#Other
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

#Local
from ScooterBackend.database.mainbase import MainBase


class Category(MainBase):

    #Колонки таблицы
    name_category: Mapped[str] = mapped_column(type_=String(250), nullable=False) #Название категории

    def __str__(self):
        #Возвращает строковый объект класса
        return str(
            dict(
                k=v
                for k, v in self.__dict__.items()
            )
        )

    def __repr__(self) -> str:
        #Возвращает строковый объект класса
        return self.__str__()