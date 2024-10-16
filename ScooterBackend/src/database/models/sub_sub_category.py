from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.mainbase import MainBase
from typing import List


class SubSubCategory(MainBase):
    """
    Таблица под под категорий
    """

    name: Mapped[str] = mapped_column(
        type_=String(length=225),
        nullable=False,
        unique=True
    )
    id_sub_category: Mapped[int] = mapped_column(
        ForeignKey("Subcategory.id"),
        type_=Integer
    )

    # Связи
    sub_category_data: Mapped["SubCategory"] = relationship(
        "SubCategory",
        back_populates="sub_sub_category_data",
        uselist=False
    )

    product_data: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="sub_sub_category_data",
        uselist=True
    )

    def __str__(self) -> str:
        return str({
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")})

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> dict:
        return {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")}
