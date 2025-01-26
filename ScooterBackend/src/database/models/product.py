# System
from typing import List, Dict
from datetime import date

# Other
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Double, Text, Date, ForeignKey

# Local
from src.database.mainbase import MainBase
from src.database.models.product_photos import ProductPhotos


class Product(MainBase):
    # Таблица продукт-товар

    # Артикул продукта
    article_product: Mapped[str] = mapped_column(
        type_=String(300), nullable=False, default=""
    )

    # Заголовок продукта
    title_product: Mapped[str] = mapped_column(
        type_=String(500),
        nullable=False,
        default="Заголовок продукта",
        unique=True,
        index=True,
    )

    # Бренд товара
    brand: Mapped[int] = mapped_column(
        ForeignKey("Brand.id", ondelete="SET NULL"),
        type_=Integer,
        nullable=True,
    )

    # Марка
    brand_mark: Mapped[int] = mapped_column(
        ForeignKey("Mark.id", ondelete="SET NULL"), type_=Integer, nullable=True
    )

    # Объемный вес продукта
    weight_product: Mapped[float] = mapped_column(
        type_=Double, nullable=True, default=0.0
    )

    # Подкатегория
    id_sub_category: Mapped[int] = mapped_column(
        ForeignKey("Subcategory.id", ondelete="SET NULL"),
        type_=Integer,
        nullable=True,
    )

    # Пояснение продукта
    explanation_product: Mapped[str] = mapped_column(
        type_=Text, nullable=True, default="Пояснение"
    )

    # Количество продукта
    quantity_product: Mapped[int] = mapped_column(
        type_=Integer, nullable=True, default=0
    )

    # Метка продукта
    label_product: Mapped[str] = mapped_column(
        type_=String(80), nullable=True, default="1 год"
    )

    # Цена продукта
    price_product: Mapped[float] = mapped_column(
        type_=Double, nullable=False, default=0
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

    # Relation's
    # Отзывы
    reviews: Mapped[List["Review"]] = relationship(
        "Review", back_populates="product", uselist=True
    )

    # Заказы
    order: Mapped[List["Order"]] = relationship(
        "Order", back_populates="product_info", uselist=True
    )

    # Избранные
    product_info_for_fav: Mapped[List["Favourite"]] = relationship(
        "Favourite", back_populates="product_info", uselist=True
    )

    # Бренд
    brand_data: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="product_data",
        uselist=False,
    )

    # Марка
    mark_data: Mapped["Mark"] = relationship(
        "Mark", back_populates="product_data", uselist=False
    )

    # Модели продукта
    product_models_data: Mapped[List["ProductModels"]] = relationship(
        "ProductModels",
        back_populates="product_data",
        uselist=True,
        cascade="all, delete",
    )

    # Данные категории
    sub_category_data: Mapped["SubCategory"] = relationship(
        "SubCategory",
        back_populates="product_data",
        uselist=False,
    )

    # Фотографии продукта
    photos: Mapped[List["ProductPhotos"]] = relationship(
        "ProductPhotos",
        back_populates="product_data",
        uselist=True,
        cascade="all, delete",
    )

    def read_model(self) -> Dict[str, str]:
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }

    def __str__(self) -> str:
        # Возвращает строковый объект класса
        return str(
            {
                "Идентификатор": self.id,
                "Название": self.title_product,
                "Бренд": self.brand,
                "Подкатегория": self.id_sub_category,
                "Цена": self.price_product,
            }
        )

    def __repr__(self) -> str:
        # Возвращает строковый объект класса
        return self.__str__()
