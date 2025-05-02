from typing import Dict, Union
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Text


# Local
from src.database.mainbase import MainBase


class VacancyRequest(MainBase):

    name_user: Mapped[str] = mapped_column(
        type_=String(length=165), nullable=False, index=False, unique=False
    )

    email_user: Mapped[str] = mapped_column(
        type_=String(length=255), nullable=False, index=False, unique=False
    )

    telephone_user: Mapped[str] = mapped_column(
        type_=String(length=75), nullable=False, index=False, unique=False
    )

    experience_user: Mapped[str] = mapped_column(
        type_=Text, nullable=True, index=False, unique=False
    )

    id_vacancy: Mapped[int] = mapped_column(
        ForeignKey("Vacancies.id", ondelete="CASCADE"), type_=Integer
    )

    vacancy_data: Mapped["Vacancies"] = relationship(
        "Vacancies", back_populates="user_requests", uselist=False
    )

    def __str__(self) -> str:
        # Возвращает строковый объект
        return str(
            {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        )

    def __repr__(self) -> str:
        # Возвращает строковый объект
        return self.__str__()

    def read_model(self) -> Dict[str, Union[str, int]]:
        # Чтение модели
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
