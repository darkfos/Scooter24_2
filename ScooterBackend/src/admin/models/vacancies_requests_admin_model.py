from sqladmin.models import ModelView
from typing import List, Any, Dict

from src.database.models.vacancy_request import VacancyRequest


class VacanciesRequestsAdminModel(ModelView, model=VacancyRequest):

    name: str = "Отклики"
    name_plural: str = "Отклик"
    icon: str = "fa fa-user-circle-o"
    category: str = "Работа"

    column_list: List[Any] = [
        VacancyRequest.name_user,
        VacancyRequest.email_user,
        VacancyRequest.telephone_user,
        VacancyRequest.experience_user,
        VacancyRequest.vacancy_data,
    ]

    column_labels: Dict[str, str] = {
        VacancyRequest.id: "Идентификатор отклика",
        VacancyRequest.id_vacancy: "Идентификатор вакансии",
        VacancyRequest.name_user: "Имя пользователя",
        VacancyRequest.email_user: "Электронная почта пользователя",
        VacancyRequest.telephone_user: "Номер телефона пользователя",
        VacancyRequest.experience_user: "Опыт пользователя",
        VacancyRequest.vacancy_data: "Данные вакансии",
    }

    form_create_rules: List[str] = [
        "name_user",
        "email_user",
        "telephone_user",
        "experience_user",
        "vacancy_data",
    ]

    column_select_related_list: List[str] = ["vacancy_data"]

    form_ajax_refs = {
        "vacancy_data": {
            "fields": ("salary_employee", "id", "description_vacancies"),
            "order_by": ("id"),
            "placeholder": "Выбрать вакансию",
        }
    }
