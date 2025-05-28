from sqladmin.models import ModelView
from src.database.models.type_worker import TypeWorker
from typing import List, Any


class TypeWorkerModelView(ModelView, model=TypeWorker):

    name: str = "Тип работника"
    name_plural: str = "Тип работника"
    icon: str = "fa fa-users"
    category: str = "Работа"

    column_list: List[Any] = [
        TypeWorker.id,
        TypeWorker.name_type,
        TypeWorker.vacancies,
    ]
    column_labels: dict = {
        TypeWorker.id: "Идентификатор типа работника",
        TypeWorker.name_type: "Название",
        TypeWorker.vacancies: "Вакансии",
    }

    column_searchable_list: List[str] = ["name_type"]

    column_sortable_list: List[str] = ["id", "name_type"]

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_excluded_columns: list = [TypeWorker.vacancies]

    form_ajax_refs: dict = {
        "vacancies": {
            "fields": (
                "id",
                "description_vacancies",
                "salary_employee",
            ),
            "order_by": ("id"),
        }
    }
