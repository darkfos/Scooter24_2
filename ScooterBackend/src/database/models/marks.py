from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.mainbase import MainBase


class Mark(MainBase):
    """
    Таблица марки
    """

    # Название марки
    name_mark: Mapped[str] = mapped_column(type_=String(length=100), nullable=False, unique=True)
    
    def __str__(self) -> str:
        return str({
            k: v
            for k, v in self.__dict__.items()
        })
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def read_model(self) -> dict:
        # Чтение модели
        return {
            k:v
            for k, v in self.__dict__.items()
        }