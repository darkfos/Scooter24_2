from fastapi import Request
from sqladmin import ModelView
from sqladmin.exceptions import SQLAdminException
import wtforms
from typing import List, Any
from src.database.models.product import Product
from src.other.image_saver import ImageSaver
from src.admin.admin_models_exceptions import NoCreateModelException
from typing import Union


class ProductModelView(ModelView, model=Product):

    #Metadata
    name: str = "Товары"
    name_plural: str = "Добавить товар"
    icon: str = "fa fa-motorcycle"
    category: str = "Товар"

    column_labels: dict = {
        Product.id: "Идентификатор продукта",
        Product.title_product: "Заголовок",
        Product.article_product: "Артикл",
        Product.explanation_product: "Описание",
        Product.tags: "Теги",
        Product.quantity_product: "Количество",
        Product.product_discount: "Скидка",
        Product.price_product: "Цена",
        Product.date_create_product: "Дата создания",
        Product.date_update_information: "Дата обновления",
        Product.photo_product: "Фотография"
    }
    
    #Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    column_exclude_list = ["order", "reviews", "product_all_categories", "product_info_for_fav"]

    form_create_rules: list = [
        "title_product", "article_product", "explanation_product", "tags", "quantity_product",
        "product_discount", "price_product", "date_create_product", "date_update_information", "photo_product"
    ]
    #Form's for FK
    form_ajax_refs: dict = {
        "reviews": {
            "fields": ("id", "id_user", "id_product", ),
            "order_by": ("id")
        },
        "order": {
            "fields":("id", "date_buy", "id_user", ),
            "order_by": ("id")
        },
        "product_all_categories": {
            "fields": ("id", "id_category", ),
            "order_by": ("id")
        },
        "product_info_for_fav": {
            "fields": ("id", ),
            "order_by": ("id")
        }
    }

    #Photo check
    form_overrides = dict(photo_product=wtforms.FileField)

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        
        #Check file
        if "image" in str(data.get("photo_product").headers["content-type"]):
            
            #Save file
            image_service = ImageSaver()
            is_saver: Union[str, None] = await image_service.save_file(file=data.get("photo_product"), is_admin=True)

            if is_saver:
                data["photo_product"] = is_saver
                return
        raise SQLAdminException("Не удалось создать модель")
    
    async def on_model_delete(self, model: Any, request: Request) -> None:
        #Delete image
        image_service = ImageSaver()
        image_service.filename = model.photo_product
        await image_service.remove_file()
        return