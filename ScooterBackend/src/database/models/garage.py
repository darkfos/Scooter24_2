from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database.mainbase import MainBase

# Local
from src.database.models.model import Model
from src.database.models.marks import Mark
from src.database.models.type_moto import TypeMoto
from src.database.models.user import User


class Garage(MainBase):

    # Идентификатор модели
    id_model: Mapped[int] = mapped_column(
        ForeignKey("Model.id"), nullable=False
    )

    # Идентификатор марки
    id_mark: Mapped[int] = mapped_column(ForeignKey("Mark.id"), nullable=False)

    # Идентификатор типа транспорта
    id_type_moto: Mapped[int] = mapped_column(
        ForeignKey("Typemoto.id"), nullable=False
    )

    # Идентификатор пользователя
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)

    user_data: Mapped["User"] = relationship(
        "User",
        back_populates="garage_data",
        uselist=False,
        cascade="all, delete",
    )
    mark_data: Mapped["Mark"] = relationship(
        "Mark",
        back_populates="garage_data",
        uselist=False,
        cascade="all, delete",
    )
    type_moto_data: Mapped["TypeMoto"] = relationship(
        "TypeMoto",
        back_populates="garage_data",
        uselist=False,
        cascade="all, delete",
    )
    model_data: Mapped["Model"] = relationship(
        "Model",
        back_populates="garage_data",
        uselist=False,
        cascade="all, delete",
    )

    def read_model(self) -> dict:
        return {
            el: self.__dict__.get(el)
            for el in self.__dict__.keys()
            if not el.startswith("_")
        }

    def __str__(self) -> str:
        return str(
            {
                el: self.__dict__.get(el)
                for el in self.__dict__.keys()
                if not el.startswith("_")
            }
        )

    def __repr__(self) -> str:
        return self.__str__()
