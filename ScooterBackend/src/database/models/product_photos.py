from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey
from src.database.mainbase import MainBase


class ProductPhotos(MainBase):

    # Ссылка на картинку
    photo_url: Mapped[str] = mapped_column(
        type_=Text, nullable=False, index=False, unique=False
    )

    # Идентификатор продукта
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id", ondelete="CASCADE")
    )

    # Информация о продукте
    product_data: Mapped["Product"] = relationship(
        "Product", back_populates="photos", uselist=False
    )

    def __str__(self):
        return str(
            {
                k: v for k, v in self.__dict__.items() if not k.startswith("_")
            }  # noqa
        )

    def __repr__(self):
        return self.__str__()

    def read_model(self) -> dict:
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }  # noqa
