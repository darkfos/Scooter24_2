from typing import List, Dict
from datetime import date

# Other
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Double, Text, Date, ForeignKey, Boolean

# Local
from src.database.mainbase import MainBase


class Product(MainBase):
    article_product: Mapped[str] = mapped_column(
        type_=String(300), nullable=False, default=""
    )

    title_product: Mapped[str] = mapped_column(
        type_=String(500),
        nullable=False,
        default="Заголовок продукта",
        unique=True,
        index=True,
    )

    brand: Mapped[int] = mapped_column(
        ForeignKey("Brand.id", ondelete="SET NULL"),
        type_=Integer,
        nullable=True,
    )

    weight_product: Mapped[float] = mapped_column(
        type_=Double, nullable=True, default=0.0
    )

    is_recommended: Mapped[bool] = mapped_column(
        type_=Boolean, nullable=True, default=False
    )

    id_sub_category: Mapped[int] = mapped_column(
        ForeignKey("Subcategory.id", ondelete="SET NULL"),
        type_=Integer,
        nullable=True,
    )

    explanation_product: Mapped[str] = mapped_column(
        type_=Text, nullable=True, default="Пояснение"
    )

    quantity_product: Mapped[int] = mapped_column(
        type_=Integer, nullable=True, default=0
    )

    label_product: Mapped[str] = mapped_column(
        type_=String(80), nullable=True, default="1 год"
    )

    price_product: Mapped[float] = mapped_column(
        type_=Double, nullable=False, default=0
    )

    date_create_product: Mapped[date] = mapped_column(
        type_=Date, nullable=True, default=date.today()
    )

    date_update_information: Mapped[date] = mapped_column(
        type_=Date, nullable=True, default=date.today()
    )

    product_discount: Mapped[int] = mapped_column(
        type_=Integer, nullable=True, default=0
    )

    reviews: Mapped[List["Review"]] = relationship(
        "Review", back_populates="product", uselist=True
    )

    orders_list: Mapped[List["OrderProducts"]] = relationship(
        "OrderProducts",
        back_populates="product_data",
        uselist=True,
        cascade="all, delete-orphan",
    )

    product_info_for_fav: Mapped[List["Favourite"]] = relationship(
        "Favourite", back_populates="product_info", uselist=True
    )

    brand_data: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="product_data",
        uselist=False,
    )

    product_models_data: Mapped[List["ProductModels"]] = relationship(
        "ProductModels",
        back_populates="product_data",
        uselist=True,
        cascade="all, delete",
    )

    sub_category_data: Mapped["SubCategory"] = relationship(
        "SubCategory",
        back_populates="product_data",
        uselist=False,
    )

    brand_mark: Mapped[List["ProductMarks"]] = relationship(
        "ProductMarks",
        back_populates="product_data",
        uselist=True,
        cascade="all, delete-orphan",
    )

    photos: Mapped[List["ProductPhotos"]] = relationship(
        "ProductPhotos",
        back_populates="product_data",
        uselist=True,
        cascade="all, delete",
    )

    type_models: Mapped[List["ProductTypeModels"]] = relationship(
        "ProductTypeModels",
        back_populates="product_data",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def read_model(self) -> Dict[str, str]:
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }

    def __str__(self) -> str:
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
        return self.__str__()
