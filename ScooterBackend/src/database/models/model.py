from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.mainbase import MainBase


class Model(MainBase):
    """
    Таблица модель
    """

    # Название модели
    name_model: Mapped[str] = mapped_column(type_=String(length=100), unique=True, nullable=False)

    def __str__(self) -> str:
        return str({
            k:v
            for k,v in self.__dict__.items()
        })
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def read_model(self) -> dict:
        # Чтение модели
        
        return {
            k: v
            for k,v in self.__dict__.items()
        }