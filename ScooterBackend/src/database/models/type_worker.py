# System
from typing import Dict, Union, List


# Other libraries
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

# Local
from src.database.mainbase import MainBase


class TypeWorker(MainBase):

    # Название типа работника
    name_type: Mapped[str] = mapped_column(
        type_=String(300),
        unique=True,
        nullable=False,
        index=True
    )

    # Relation
    vacancies: Mapped[List["Vacancies"]] = relationship(
        "Vacancies",
        uselist=True,
        back_populates="type_work"
    )

    def __str__(self) -> str:
        # Возвращает строковый объект
        return str(
            {k: v for k, v in self.__dict__.items()
             if not k.startswith("_")}
        )

    def __repr__(self) -> str:
        # Возвращает строковый объект
        return self.__str__()

    def read_model(self) -> Dict[str, Union[str, int]]:
        # Чтение модели
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith("_")}
