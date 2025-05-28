from typing import Dict, Union, List


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from src.database.mainbase import MainBase


class TypeWorker(MainBase):

    name_type: Mapped[str] = mapped_column(
        type_=String(300), unique=True, nullable=False, index=True
    )

    vacancies: Mapped[List["Vacancies"]] = relationship(
        "Vacancies",
        uselist=True,
        back_populates="type_work",
        cascade="all, delete",
    )

    def __str__(self) -> str:
        return str({"Идентификатор": self.id, "Название": self.name_type})

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> Dict[str, Union[str, int]]:
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
