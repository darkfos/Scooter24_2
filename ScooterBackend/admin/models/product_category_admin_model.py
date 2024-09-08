from sqladmin.models import ModelView
from typing import List, Any
from database.models.product_category import ProductCategory


class ProductCategoryModelView(ModelView, model=ProductCategory):

    #Metadata
    name: str = "Категории продукта"
    name_plural: str = "Добавление категории"
    icon: str = "fa-puzzle-piece"
    category: str = "Товар"

    column_list: List[Any] = [ProductCategory.id, ProductCategory.id_category, ProductCategory.id_product,
                              ProductCategory.category_information, ProductCategory.product_information]
    
    #Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    #Form's for FK
    form_ajax_refs: dict = {
        "category_information": {
            "fields": ("id", "name_category"),
            "order_by": ("id")
        },
        "product_information": {
            "fields": ("id", "title_product"),
            "order_by": ("id")
        }
    }