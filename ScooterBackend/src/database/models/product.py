# System
from typing import List, Dict
from datetime import date

# Other
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Double, Text, Date

# Local
from src.database.mainbase import MainBase


class Product(MainBase):
    # Таблица продукт-товар

    # Заголовок продукта
    title_product: Mapped[str] = mapped_column(
        type_=String(500),
        nullable=False,
        default="Заголовок продукта",
        unique=True,
        index=True,
    )

    # Цена продукта
    price_product: Mapped[float] = mapped_column(
        type_=Double, nullable=False, default=0
    )

    # Количество продукта
    quantity_product: Mapped[int] = mapped_column(
        type_=Integer, nullable=True, default=0
    )

    # Пояснение продукта (к количеству)
    explanation_product: Mapped[str] = mapped_column(
        type_=String(780), nullable=True, default="Пояснение"
    )

    # Артикул продукта
    article_product: Mapped[str] = mapped_column(
        type_=String(300), nullable=False, default=""
    )

    # Метки продукта
    tags: Mapped[str] = mapped_column(type_=Text, nullable=True, default="")

    # Вес продукта
    other_data: Mapped[str] = mapped_column(type_=Text, nullable=True, default="")

    # Фотография продукта
    photo_product: Mapped[bytes] = mapped_column(
        type_=Text, nullable=True, default=None
    )

    # Дата создания
    date_create_product: Mapped[date] = mapped_column(
        type_=Date, nullable=True, default=date.today()
    )

    # Дата обновления информации
    date_update_information: Mapped[date] = mapped_column(
        type_=Date, nullable=True, default=date.today()
    )

    # Скидка на товар
    product_discount: Mapped[int] = mapped_column(
        type_=Integer, nullable=True, default=0
    )

    # Связи к таблицам
    reviews: Mapped[List["Review"]] = relationship(
        "Review", back_populates="product", uselist=True
    )  # Отзывы
    order: Mapped[List["Order"]] = relationship(
        "Order", back_populates="product_info", uselist=True
    )  # Заказы
    product_info_for_fav: Mapped[List["Favourite"]] = relationship(
        "Favourite", back_populates="product_info", uselist=True
    )  # Избр.
    product_all_categories: Mapped[List["ProductCategory"]] = relationship(
        "ProductCategory", back_populates="product_information", uselist=True
    )

    def read_model(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"}

    def __str__(self) -> str:
        # Возвращает строковый объект класса
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        # Возвращает строковый объект класса
        return self.__str__()
