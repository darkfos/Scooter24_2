from sqladmin import ModelView
from src.database.models.product_marks import ProductMarks
from typing import List, Any, Dict


class ProductMarksAdminModel(ModelView, model=ProductMarks):

    # Metadata
    name: str = "Марки продукта"
    name_plural: str = "Марки продукта"
    icon: str = "fa fa-tags"
    category: str = "Продукт"

    column_list: List[Any] = [
        ProductMarks.id,
        ProductMarks.id_mark,
        ProductMarks.id_product,
        ProductMarks.mark_data,
        ProductMarks.product_data,
    ]

    column_labels: dict = {
        ProductMarks.id: "Идентификатор",
        ProductMarks.id_mark: "Идентификатор марки",
        ProductMarks.id_product: "Идентификатор продукта",
        ProductMarks.mark_data: "Марки",
        ProductMarks.product_data: "Товары",
    }

    column_searchable_list: List[str] = [
        "id_mark", "id_product",
        "mark_data.name_mark", "product_data.title_product"
    ]

    column_sortable_list: List[str] = [
        "id", "id_mark", "id_product"
    ]

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules = ["name_category", "icon_category"]
    form_edit_rules = form_create_rules.copy()
    form_columns: list = [
        ProductMarks.id,
        ProductMarks.id_product,
        ProductMarks.id_mark,
    ]

    form_ajax_refs: Dict[str, dict] = {
        "mark_data": {
            "fields": (
                "id",
                "name_mark",
            ),
            "order_by": ("id", "name_mark"),
        },
        "product_data": {
            "fields": (
                "id",
                "title_product",
            ),
            "order_by": ("id", "title_product"),
        },
    }
