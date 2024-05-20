#Other
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

#Local
from ScooterBackend.database.mainbase import MainBase


class Review(MainBase):
    #Таблица отзывов

    #Текст отзыва
    text_review: Mapped[str] = mapped_column(type_=Text, default="", nullable=False)

    #Оценка товара
    estimation_review: Mapped[int] = mapped_column(type_=Integer, default=1, nullable=True)

    #Пользователь - id
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id"), type_=Integer)

    #Связи с таблицами
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")

    def __str__(self) -> str:
        #Возвращает строковый объект класса
        return str(
            {
                k: v
                for k, v in self.__dict__.items()
            }
        )

    def __repr__(self) -> str:
        #Возвращает строковый объект класса
        return self.__str__()