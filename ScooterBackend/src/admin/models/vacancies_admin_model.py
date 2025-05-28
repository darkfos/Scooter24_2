from sqladmin.models import ModelView
from src.database.models.vacancies import Vacancies
from typing import List, Any


class VacanciesModelView(ModelView, model=Vacancies):

    name: str = "Вакансии"
    name_plural: str = "Вакансия"
    icon: str = "fa fa-user-plus"
    category: str = "Работа"

    column_list: List[Any] = [
        Vacancies.id,
        Vacancies.description_vacancies,
        Vacancies.id_type_worker,
        Vacancies.salary_employee,
        Vacancies.type_work,
    ]
    column_labels: dict = {
        Vacancies.id: "Идентификатор вакансии",
        Vacancies.id_type_worker: "Идентификатор типа работника",
        Vacancies.description_vacancies: "Описание",
        Vacancies.salary_employee: "Заработная плата",
        Vacancies.type_work: "Тип работника",
    }

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    column_searchable_list: List[str] = [
        "id_type_worker",
        "description_vacancies",
        "salary_employee",
        "type_work",
    ]

    column_sortable_list: List[str] = [
        "id",
        "id_type_worker",
        "salary_employee",
        "description_vacancies",
    ]

    form_ajax_refs: dict = {
        "type_work": {
            "fields": (
                "id",
                "name_type",
            ),
            "order_by": ("id"),
        }
    }
