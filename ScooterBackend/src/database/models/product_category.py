# Local
from src.database.mainbase import MainBase

# Other
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey


class ProductCategory(MainBase):

    id_product: Mapped[int] = mapped_column(ForeignKey("Product.id"), type_=Integer)
    id_category: Mapped[int] = mapped_column(ForeignKey("Category.id"), type_=Integer)

    product_information: Mapped["Product"] = relationship(
        "Product", back_populates="product_all_categories", uselist=False
    )
    category_information: Mapped["Category"] = relationship(
        "Category", back_populates="category_data", uselist=False
    )

    def read_model(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"}

    def __str__(self) -> str:
        return str(self.read_model())

    def __repr__(self) -> str:
        return self.__str__()
