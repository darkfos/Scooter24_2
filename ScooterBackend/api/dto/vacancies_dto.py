#System
from typing import Annotated

#Other libraries
from pydantic import BaseModel, Field


class VacanciesBase(BaseModel):

    salary_employee: Annotated[int, Field(gt=0)]
    description_vacancies: Annotated[str, Field(gt=0)]
    id_type_worker: Annotated[int, Field()]


class UpdateVacancies(BaseModel):
    id: int
    salary_employee: Annotated[int, Field(gt=0)]
    description_vacancies: Annotated[str, Field(gt=0)]