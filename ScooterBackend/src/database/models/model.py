from sqlalchemy import String, ForeignKey, Integer

from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.mainbase import MainBase
from typing import List


class Model(MainBase):

    name_model: Mapped[str] = mapped_column(
        type_=String(length=100), unique=True, nullable=False
    )

    id_mark: Mapped[int] = mapped_column(
        ForeignKey("Mark.id", ondelete="CASCADE"),
        type_=Integer,
        nullable=False,
    )

    product_models_data: Mapped[List["ProductModels"]] = relationship(
        "ProductModels",
        back_populates="model_data",
        uselist=True,
        cascade="all, delete",
    )
    mark_data: Mapped["Mark"] = relationship(
        "Mark", back_populates="model_data", uselist=False
    )

    garage_data: Mapped[List["Garage"]] = relationship(
        "Garage",
        back_populates="model_data",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return str({"Идентификатор": self.id, "Название": self.name_model})

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> dict:
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
