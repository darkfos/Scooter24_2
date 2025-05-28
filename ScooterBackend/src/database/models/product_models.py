from src.database.mainbase import MainBase
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Dict, Union


class ProductModels(MainBase):
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id", ondelete="CASCADE"),
        type_=Integer,
        nullable=False,
    )
    id_model: Mapped[int] = mapped_column(
        ForeignKey("Model.id", ondelete="CASCADE"),
        type_=Integer,
        nullable=False,
    )

    product_data: Mapped["Product"] = relationship(
        "Product", back_populates="product_models_data", uselist=False
    )
    model_data: Mapped["Model"] = relationship(
        "Model", back_populates="product_models_data", uselist=False
    )

    def __str__(self) -> str:
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(
        self,
    ) -> Dict[str, Union[int, str, List[Union[int, str, dict]]]]:
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
