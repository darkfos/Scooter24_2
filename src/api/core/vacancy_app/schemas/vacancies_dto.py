# System
from typing import Annotated, List, Dict, Union

# Other libraries
from pydantic import BaseModel, Field, EmailStr


class VacanciesBase(BaseModel):
    """
    DTO - Базовый объект для работы с вакансиями
    """

    salary_employee: Annotated[int, Field(gt=0)]
    description_vacancies: Annotated[str, Field(min_length=0)]
    is_worked: Annotated[Union[None, str], Field()]
    type_work: Annotated[Dict, Field()]
    id_vacancy: int


class UpdateVacancies(BaseModel):
    """
    DTO - Обновление вакансии
    """

    id: int
    salary_employee: Annotated[int, Field(gt=0)] = None
    description_vacancies: Annotated[str, Field(gt=0)] = None


class VacanciesGeneralData(BaseModel):
    """
    DTO - Главная информация о вакансии
    """

    vacancies: Annotated[List[VacanciesBase], Field()]


class RequestVacancy(BaseModel):
    """
    DTO -  Создание отклика на вакансию
    """

    name_user: Annotated[str, Field(max_length=165)]
    email_user: Annotated[EmailStr, Field(max_length=255)]
    telephone_user: Annotated[str, Field(max_length=75)]
    experience_user: Annotated[Union[str, None], Field(default=None)]
    id_vacancy: Annotated[int, Field()]
