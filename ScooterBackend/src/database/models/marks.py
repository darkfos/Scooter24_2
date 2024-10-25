from sqlalchemy import String
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.mainbase import MainBase


class Mark(MainBase):
    """
    Таблица марки
    """

    # Название марки
    name_mark: Mapped[str] = mapped_column(
        type_=String(length=100), nullable=False, unique=True
    )

    # Связи
    product_data: Mapped["Product"] = relationship(
        "Product", back_populates="mark_data", uselist=False
    )
    model_data: Mapped[List["Model"]] = relationship(
        "Model", back_populates="mark_data", uselist=True
    )

    def __str__(self) -> str:
        return str({"Идентификатор": self.id, "Название": self.name_mark})

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> dict:
        # Чтение модели
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
