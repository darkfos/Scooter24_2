# System
from typing import Dict, Union


# Other libraries
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Text

# Local
from src.database.mainbase import MainBase


class Vacancies(MainBase):

    # Заработная плата для вакансии
    salary_employee: Mapped[int] = mapped_column(
        type_=Integer, nullable=False, unique=False, index=False
    )

    # Описание вакансии
    description_vacancies: Mapped[str] = mapped_column(
        type_=Text, nullable=False, unique=False, index=False
    )

    # Relations
    id_type_worker: Mapped[int] = mapped_column(
        ForeignKey("Typeworker.id"), type_=Integer
    )
    type_work: Mapped["TypeWorker"] = relationship(
        "TypeWorker", uselist=False, back_populates="vacancies"
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
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
