from src.database.mainbase import MainBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Dict, List


class UserType(MainBase):

    name_type: Mapped[str] = mapped_column(type_=String(length=100))

    # Связи
    user_data: Mapped[List["User"]] = relationship(
        "User",
        back_populates="type_user_data",
        uselist=True
    )

    def __str__(self) -> str:
        return str({k: v for k, v in self.__dict__.items()})

    def __repr__(self) -> str:
        return self.__str__()

    def read_model(self) -> Dict:
        return {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        }
