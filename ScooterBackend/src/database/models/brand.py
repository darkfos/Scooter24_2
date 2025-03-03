from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.mainbase import MainBase


class Brand(MainBase):
    """
    Таблица Бренды
    """

    # Название бренда
    name_brand: Mapped[str] = mapped_column(
        type_=String(length=100), nullable=False, unique=True
    )

    # Ссылка на фотографию бренда
    url_photo: Mapped[str] = mapped_column(
        type_=Text, nullable=True, unique=False
    )

    # Связи
    product_data: Mapped["Product"] = relationship(
        "Product",
        back_populates="brand_data",
        uselist=False,
    )

    def __str__(self) -> str:
        return str({"Идентификатор": self.id, "Название": self.name_brand})

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> dict:
        """
        Чтение модели
        """

        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
