from sqladmin import ModelView
from src.database.models.garage import Garage
from typing import List, Any, Dict


class GarageAdminModel(ModelView, model=Garage):

    # Metadata
    name: str = "Гараж"
    name_plural: str = "Гараж пользователя"
    icon: str = "fa fa-tags"
    category: str = "Продукт"

    column_list: List[Any] = [
        Garage.id,
        Garage.id_model,
        Garage.id_mark,
        Garage.id_user,
        Garage.id_type_moto,
        Garage.mark_data,
        Garage.user_data,
        Garage.model_data,
        Garage.type_moto_data,
    ]

    column_labels: dict = {
        Garage.id: "Идентификатор",
        Garage.id_model: "Модель",
        Garage.id_mark: "Марка",
        Garage.id_user: "Пользователь",
        Garage.id_type_moto: "Мототранспорт",
        Garage.mark_data: "Марка",
        Garage.user_data: "Пользователь",
        Garage.model_data: "Модель",
        Garage.type_moto_data: "Данные типа модели",
    }

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules = ["id_model", "id_mark", "id_user", "id_type_moto"]
    form_edit_rules = form_create_rules.copy()
    form_columns: list = [
        Garage.id,
        Garage.id_mark,
        Garage.id_model,
        Garage.id_user,
        Garage.id_type_moto,
    ]

    form_ajax_refs: Dict[str, dict] = {
        "mark_data": {
            "fields": (
                "id",
                "name_mark",
            ),
            "order_by": ("id", "name_mark"),
        },
        "user_data": {
            "fields": (
                "id",
                "name_user",
            ),
            "order_by": ("id", "name_user"),
        },
        "model_data": {
            "fields": ("id", "name_model"),
            "order_by": ("id", "name_model"),
        },
        "type_moto_data": {
            "fields": ("id", "name_moto_type"),
            "order_by": ("id", "name_moto_type"),
        },
    }
