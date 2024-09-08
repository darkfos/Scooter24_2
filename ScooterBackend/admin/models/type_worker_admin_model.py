from sqladmin.models import ModelView
from database.models.type_worker import TypeWorker
from typing import List, Any


class TypeWorkerModelView(ModelView, model=TypeWorker):

    #Metadata
    name: str = "Тип работника"
    name_plural: str = "Добавить тип работника"
    icon: str = "fa-users"
    category: str = "Пользователь"

    column_list: List[Any] = [TypeWorker.id, TypeWorker.name_type, TypeWorker.vacancies]

    #Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    #Form's for FK
    form_ajax_refs: dict = {
        "vacancies": {
            "fields": ("id", "description_vacancies", "salary_employee"),
            "order_by": ("id")
        }
    }