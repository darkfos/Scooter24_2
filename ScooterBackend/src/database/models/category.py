# System
from typing import List, Dict

# Other
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

# Local
from src.database.mainbase import MainBase


class Category(MainBase):
    # Таблица категории товаров

    # Колонки таблицы
    name_category: Mapped[str] = mapped_column(
        type_=String(150), nullable=False, unique=True, index=True
    )

    icon_category: Mapped[str] = mapped_column(
        type_=Text,
        nullable=True,
        index=False,
    )

    # Связи
    subcategory_data: Mapped[List["SubCategory"]] = relationship(
        "SubCategory",
        back_populates="category_data",
        uselist=True,
        cascade="all, delete",
    )

    def read_model(self) -> Dict[str, str]:
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }

    def __str__(self):
        # Возвращает строковый объект класса
        return str({"Идентификатор": self.id, "Название": self.name_category})

    def __repr__(self) -> str:
        # Возвращает строковый объект класса
        return self.__str__()
