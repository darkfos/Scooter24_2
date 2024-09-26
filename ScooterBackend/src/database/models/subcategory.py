from src.database.mainbase import MainBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import List


class SubCategory(MainBase):

    name: Mapped[str] = mapped_column(type_=String(length=225), nullable=False)
    level: Mapped[int] = mapped_column(type_=Integer)
    id_category: Mapped[int] = mapped_column(ForeignKey("Category.id"), type_=Integer)
    id_sub_category: Mapped[int] = mapped_column(ForeignKey("Subcategory.id"), type_=Integer)

    #relation's
    category_data: Mapped["Category"] = relationship("Category", back_populates="sub_category_data", uselist=False)
    product_data_1: Mapped[List["Product"]] = relationship("Product", back_populates="sub_category_data", uselist=True)
    product_data_2: Mapped[List["Product"]] = relationship("Product", back_populates="sub_l2_category_data", uselist=True)

    def __str__(self) -> str:
        return str({
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith('_')
        })
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def read_model(self) -> dict:
        return {
            k: v
            for k,v in self.__dict__.items()
            if not k.startswith("_")
        }