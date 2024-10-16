# System
from typing import Dict

# Other
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

# Local
from src.database.mainbase import MainBase


class Review(MainBase):
    # Таблица отзывов

    # Текст отзыва
    text_review: Mapped[str] = mapped_column(
        type_=Text,
        default="",
        nullable=False
    )

    # Оценка товара
    estimation_review: Mapped[int] = mapped_column(
        type_=Integer,
        default=1,
        nullable=False
    )

    # Пользователь - id
    id_user: Mapped[int] = mapped_column(
        ForeignKey("User.id"),
        type_=Integer
    )
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id"),
        type_=Integer
    )

    # Связи с таблицами
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews",
        uselist=False
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews",
        uselist=False
    )

    def read_model(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()
                if k != "_sa_instance_state"}

    def __str__(self) -> str:
        # Возвращает строковый объект класса
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        # Возвращает строковый объект класса
        return self.__str__()
