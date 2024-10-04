from fastapi import Request
from sqladmin import ModelView
from sqladmin.exceptions import SQLAdminException
from src.database.models.category import Category
from src.other.image.image_saver import ImageSaver
from typing import List, Any, Coroutine, Tuple
import wtforms


class CategoryModelView(ModelView, model=Category):

    # Metadata
    name: str = "Категории"
    name_plural: str = "Категории"
    icon: str = "fa fa-tags"
    category: str = "Продукт"

    column_list: List[Any] = [Category.id, Category.name_category, Category.icon_category, Category.subcategory_data]
    column_labels: dict = {
        Category.id: "Идентификатор категории",
        Category.name_category: "Название категории",
        Category.subcategory_data: "Подкатегория",
    }

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules = ["name_category", "icon_category"]
    form_edit_rules = form_create_rules.copy()

    form_overrides: dict = dict(icon_category=wtforms.FileField)

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        if "image" in str(data.get("icon_category").headers["Content-Type"]):

            img_saver: ImageSaver = ImageSaver()
            is_saver = await img_saver.save_file(
                file=data.get("icon_category"),
                is_admin=True
            )

            if is_saver:
                data["icon_category"] = is_saver
                return 
        raise SQLAdminException("Не удалось создать, изменить запись")
    
    async def on_model_delete(self, model: Any, request: Request) -> None:
        
        img_saver: ImageSaver = ImageSaver()
        img_saver.filename = model.icon_category
        if img_saver.filename:
            await img_saver.remove_file()
            return
    
    async def get_detail_value(self, obj: Any, prop: str) -> Coroutine[Any, Any, Tuple[Any, Any]]:

        if prop == "icon_category":
            prev_obj_photo_data = obj.icon_category
            formatted_value: dict[str, str] = {
                "type": "image",
                "src": f"/static/images/{prev_obj_photo_data}",
                "alt": "Фотография продукта",
                "style": "width: 400px; height: auto"
            }
            return prev_obj_photo_data, formatted_value
        return await super().get_detail_value(obj, prop)