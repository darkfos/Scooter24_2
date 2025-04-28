from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.mainbase import MainBase


class ProductTypeModels(MainBase):

    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id", ondelete="CASCADE"),
        type_=Integer,
        nullable=False,
        unique=False,
        index=False,
    )

    id_type_model: Mapped[int] = mapped_column(
        ForeignKey("Typemoto.id", ondelete="CASCADE"),
        type_=Integer,
        nullable=False,
        unique=False,
        index=False,
    )

    # Связи
    product_data: Mapped["Product"] = relationship(
        "Product", back_populates="type_models", uselist=False
    )

    type_models_data: Mapped["TypeMoto"] = relationship(
        "TypeMoto", back_populates="product_type_models", uselist=False
    )

    def read_model(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    def __repr__(self) -> str:
        return self.__str__()
