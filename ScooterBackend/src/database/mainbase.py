from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)
from sqlalchemy import Integer


class MainBase(DeclarativeBase):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.title()
