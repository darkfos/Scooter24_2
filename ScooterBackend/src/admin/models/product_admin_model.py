from sqladmin import ModelView
from typing import List, Any
from src.database.models.product import Product


class ProductModelView(ModelView, model=Product):

    #Metadata
    name: str = "Товары"
    name_plural: str = "Добавить товар"
    icon: str = "fa-motorcycle"
    category: str = "Товар"

    column_list: List[Any] = [Product.id, Product.title_product, Product.article_product,
                              Product.date_create_product, Product.date_update_information, Product.explanation_product,
                              Product.tags, Product.quantity_product, Product.product_discount, Product.price_product,
                              Product.product_info_for_fav, Product.other_data]
    
    #Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    #Form's for FK
    form_ajax_refs: dict = {
        "reviews": {
            "fields": ("id", "id_user", "id_product", ),
            "order_by": ("id", )
        },
        "order": {
            "fields":("id", "date_buy", "id_user", ),
            "order_by": ("id", )
        },
        "product_all_categories": {
            "fields": ("id", "id_category", ),
            "order_by": ("id", )
        }
    }