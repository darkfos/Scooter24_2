from sqladmin import ModelView
from database.models.type_moto import TypeMoto


class TypeMotoAdminModel(ModelView, model=TypeMoto):

    # Metadata
    name: str = "Тип"
    name_plural: str = "Мототранспорт"
    icon: str = "fa fa-motorcycle"
    category: str = "Продукт"

    column_list: list = [
        TypeMoto.id,
        TypeMoto.name_moto_type,
        TypeMoto.product_type_models,
        TypeMoto.garage_data,
    ]

    column_labels: dict = {
        TypeMoto.id: "Идентификатор",
        TypeMoto.name_moto_type: "Название",
        TypeMoto.product_type_models: "Товары",
        TypeMoto.garage_data: "Гараж",
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules: list = [
        "id",
        "name_moto_type",
    ]

    form_edit_rules = form_create_rules.copy()

    # Form's for FK
    form_ajax_refs: dict = {
        "product_type_models": {
            "fields": ("id", "id_product"),
            "order_by": ("id", "id_product"),
        },
        "garage_data": {
            "fields": ("id", "id_mark", "id_model"),
            "order_by": ("id", "id_mark"),
        },
    }
