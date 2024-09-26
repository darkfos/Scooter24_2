from fastapi import Request
from sqladmin import ModelView
from sqladmin.exceptions import SQLAdminException
import wtforms
from typing import Coroutine, List, Any, Tuple
from src.database.models.product import Product
from src.other.image.image_saver import ImageSaver
from typing import Union


class ProductModelView(ModelView, model=Product):

    # Metadata
    name: str = "Товары"
    name_plural: str = "Товар"
    icon: str = "fa fa-motorcycle"
    category: str = "Товар"

    column_list: list = [Product.id, Product.id_category, Product.id_subcategory_thirst_level, Product.id_subcategory_second_level, Product.brand,
                         Product.brand_mark, Product.model, Product.title_product, Product.article_product, Product.explanation_product,
                         Product.weight_product, Product.quantity_product, Product.price_product, Product.price_with_discount, Product.date_create_product,
                         Product.date_update_information, Product.photo_product, Product.category_data, Product.sub_category_datas, Product.sub_l2_category_data,
                         Product.order, Product.reviews, Product.product_info_for_fav]

    column_labels: dict = {
        Product.id: "Идентификатор продукта",
        Product.id_category: "Категория",
        Product.id_subcategory_thirst_level: "Подкатегория 1ур",
        Product.id_subcategory_second_level: "Подкатегория 2ур",
        Product.brand: "Бренд",
        Product.brand_mark: "Марка",
        Product.model: "Модель",
        Product.title_product: "Заголовок",
        Product.article_product: "Артикл",
        Product.explanation_product: "Описание",
        Product.weight_product: "Объемный вес продукта",
        Product.quantity_product: "Количество",
        Product.product_discount: "Скидка",
        Product.price_product: "Цена без скидки",
        Product.price_with_discount: "Цена со скидкой",
        Product.date_create_product: "Дата создания",
        Product.date_update_information: "Дата обновления",
        Product.photo_product: "Фотография",
        Product.category_data: "Категория",
        Product.sub_category_datas: "Подкатегория 1 уровня",
        Product.sub_l2_category_data: "Подкатегория 2 уровня"
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules: list = [
        "id_category",
        "id_subcategory_thirst_level",
        "id_subcategory_second_level",
        "title_product",
        "article_product",
        "explanation_product",
        "quantity_product",
        "product_discount",
        "weight_product",
        "price_product",
        "price_with_discount",
        "date_create_product",
        "date_update_information",
        "photo_product",
        "brand",
        "brand_mark",
        "model",
        "category_data",
        "sub_category_datas",
        "sub_l2_category_data"
    ]

    # Form's for FK
    form_ajax_refs: dict = {
        "reviews": {
            "fields": (
                "id",
                "id_user",
                "id_product",
            ),
            "order_by": ("id"),
        },
        "order": {
            "fields": (
                "id",
                "date_buy",
                "id_user",
            ),
            "order_by": ("id"),
        },
        "product_info_for_fav": {"fields": ("id",), "order_by": ("id")},
        "category_data": {"fields": ("id", ), "order_by": ("id")},
        "sub_category_datas": {"fields": ("id", ), "order_by": ("id")},
        "sub_l2_category_data": {"fields": ("id", ), "order_by": ("id")}
    }

    # Photo check
    form_overrides = dict(photo_product=wtforms.FileField)  

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
                
        # Check file
        if "image" in str(data.get("photo_product").headers["content-type"]):

            # Save file
            image_service = ImageSaver()
            is_saver: Union[str, None] = await image_service.save_file(
                file=data.get("photo_product"), is_admin=True
            )

            if is_saver:
                data["photo_product"] = is_saver
                return
        raise SQLAdminException("Не удалось создать модель")

    async def on_model_delete(self, model: Any, request: Request) -> None:
        # Delete image
        image_service = ImageSaver()
        image_service.filename = model.photo_product
        await image_service.remove_file()
        return

    async def get_detail_value(self, obj: Any, prop: str) -> Coroutine[Any, Any, Tuple[Any, Any]]:

        if prop == "photo_product":
            prev_obj_photo_data = obj.photo_product
            formatted_value: dict[str, str] = {
                "type": "image",
                "src": f"/static/images/{prev_obj_photo_data}",
                "alt": "Фотография продукта",
                "style": "width: 400px; height: auto"
            }
            return prev_obj_photo_data, formatted_value
        return await super().get_detail_value(obj, prop)