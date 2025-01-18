from src.database.mainbase import MainBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import List


class SubCategory(MainBase):

    name: Mapped[str] = mapped_column(
        type_=String(length=225), nullable=False, unique=True
    )
    id_category: Mapped[int] = mapped_column(
        ForeignKey("Category.id", ondelete="CASCADE"),
        type_=Integer,
        nullable=False,
    )

    # Связи

    category_data: Mapped["Category"] = relationship(
        "Category", back_populates="subcategory_data", uselist=False
    )
    product_data: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="sub_category_data",
        uselist=True,
        passive_deletes=True
    )

    def __str__(self) -> str:
        return str(
            {
                "Идентификатор": self.id,
                "Название": self.name,
                "Категория": self.id_category,
            }
        )

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
