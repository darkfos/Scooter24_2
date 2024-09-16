#System
from datetime import datetime
from typing import Dict, Union

#Other libraries
from sqlalchemy import String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column

#Local
from src.database.mainbase import MainBase
from datetime import date


class Admin(MainBase):

    email_admin: Mapped[str] = mapped_column(type_=String(150), unique=True, nullable=False, index=True)
    password_user: Mapped[str] = mapped_column(type_=Text, unique=False, nullable=False)
    date_create: Mapped[date] = mapped_column(type_=Date, unique=False, nullable=True, default=date.today())
    date_update: Mapped[date] = mapped_column(type_=Date, unique=False, nullable=True, default=date.today())

    def read_model(self) -> Dict[str, Union[str, int, datetime.date]]:
        """
        Возвращает модель удобную для работы
        :return:
        """

        return {
            k: v
                for k,v in self.__dict__.items()
                if k != "_sa_instance_state"
        }

    def __str__(self):
        return str(
            {
                k: v
                for k, v in self.__dict__.items()
            }
        )

    def __repr__(self):
        return self.__str__()