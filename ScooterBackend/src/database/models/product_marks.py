from src.database.mainbase import MainBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey


class ProductMarks(MainBase):

    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id", ondelete="CASCADE"), type_=Integer, nullable=False,
    )

    id_mark: Mapped[int] = mapped_column(
        ForeignKey("Mark.id", ondelete="CASCADE"), type_=Integer, nullable=False
    )

    # Связи
    product_data: Mapped["Product"] = relationship(
        "Product", back_populates="mark_data", uselist=False
    )

    mark_data: Mapped["Mark"] = relationship(
        "Mark", back_populates="product_marks_data", uselist=False
    )

    def read_model(self):
        return {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        }

    def __str__(self):
        return str({
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        })

    def __repr__(self):
        return self.__str__()