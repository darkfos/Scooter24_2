from sqladmin import Admin, ModelView
from starlette.routing import Route, Mount
from starlette.responses import RedirectResponse, Response
from starlette.applications import Starlette
from fastapi import status, UploadFile
from starlette.staticfiles import StaticFiles
from sqladmin.authentication import login_required
from typing import Type, List
from src.database.db_worker import db_work
from fastapi import FastAPI, Request
from src.settings.engine_settings import Settings
from io import BytesIO, StringIO
from typing import override

# Models
from src.admin import all_models

# Admin Authentication
from src.admin.admin_auth import AdminPanelAuthentication
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import EngineRepository
from fastapi import Request
from src.database.models.product import Product
from src.database.models.category import Category
from src.database.models.subcategory import SubCategory
import pandas
from sqladmin.exceptions import SQLAdminException


class AdminPanel:
    def __init__(self, app: FastAPI) -> None:
        self.admin_panel_auth: Type[AdminPanelAuthentication] = (
            AdminPanelAuthentication(
                secret_key=Settings.auth_settings.jwt_secret_key,
                auth_service=Authentication(),
            )
        )

        self.statics_scooter24 = StaticFiles(directory="src/statics")
        self.admin_panel: Type[Admin] = Admin(
            # Set settings
            engine=db_work.db_engine,
            app=app,
            title="Scooter24",
            logo_url="/static/images/scooter-logo.png",
            authentication_backend=self.admin_panel_auth,
        )

        #Admin starlette data
        self.starlette_data: Starlette = self.admin_panel.__dict__["admin"]

        #Add router
        self.starlette_data.routes.append(
            Route(path="/load_data/{model}", endpoint=self.load_data, name="load_data", methods=["POST", "GET"])
        )
        self.starlette_data.routes.append(
            Mount(path="/static_sc24", app=self.statics_scooter24, name="static_sc24")
        )

        # initialize
        self.initialize_models_view(models=all_models)

    def initialize_models_view(self, models: List[ModelView]) -> None:
        for model in models:
            self.admin_panel.add_view(model)
    
    @override
    @login_required
    async def index(self, request: Request) -> Response:
        """Index route which can be overridden to create dashboards."""
        request.session["error_message"] = ""
        request.session["warning_message"] = ""
        return await self.templates.TemplateResponse(request, "sqladmin/index.html")

    @login_required
    async def load_data(self, request: Request):

        # form data
        file: UploadFile  = (await request.form()).get("csv_file")

        if file:
            if ".csv" in file.filename or ".xlsx" in file.filename:
                file_data = (await file.read()).decode("UTF-8")

                file_object = StringIO(file_data)
                file_data = pandas.read_csv(file_object, comment="#", sep=";")
                df = pandas.DataFrame(file_data)
                session = EngineRepository()
                
                cnt_to_add: int = 0
                cnt_row: int = 0


                async with session:
                    session: EngineRepository = session

                    try:
                        for index, row in df.iterrows():

                            category_data = id_subcat_1 = id_subcat_2 = None

                            if str(row["Категория"]) not in (None, "nan"):
                                category_data: Category = await session.category_repository.find_by_name(category_name=row["Категория"])
                            if str(row["Подкатегория первого уровня"]) not in (None, "nan"):
                                id_subcat_1: SubCategory = await session.subcategory_repository.find_by_name(name_subcategory=row["Подкатегория первого уровня"])
                            if str(row["Подкатегория второго уровня"]) not in (None, "nan"):
                                id_subcat_2: SubCategory = await session.subcategory_repository.find_by_name(name_subcategory=row["Подкатегория второго уровня"])

                            weight_product=float(str(row["Объемный вес, кг"]).replace("'", ""))
                            quantity_product=int(row["Доступно к продаже по схеме FBS, шт."])
                            price_product=float(row["Цена до скидки (перечеркнутая цена), ₽"])
                            price_with_discount=float(row["Текущая цена с учетом скидки, ₽"])

                            res_to_add = await session.product_repository.add_one(
                                Product(
                                        article_product=row["Артикул"],
                                        title_product=row["Наименование товара"],
                                        brand=row["Бренд"] if str(row["Бренд"]) not in (None, "nan") else "Неопределен",
                                        weight_product=weight_product,
                                        id_category=category_data.id if type(category_data) is Category else None,
                                        id_subcategory_thirst_level=id_subcat_1.id if type(id_subcat_1) is SubCategory else None,
                                        id_subcategory_second_level=id_subcat_2.id if type(id_subcat_2) is SubCategory else None,
                                        explanation_product=row["Описание"] if str(row["Описание"]) not in (None, "nan") else "Неопределен",
                                        brand_mark=row["Марка"] if str(row["Марка"]) not in (None, "nan") else "Неопределен",
                                        model=row["Модель"] if str(row["Модель"]) not in (None, "nan") else "Неопределен",
                                        photo_product=row["Фото"] if str(row["Фото"]) not in (None, "nan") else "Неопределен",
                                        quantity_product=quantity_product,
                                        price_product=price_product,
                                        price_with_discount=price_with_discount,
                                        product_discount=0,
                                )
                            )

                            if res_to_add: cnt_to_add += 1
                            cnt_row += 1
                    except KeyError as ke:
                        model_view = "product" if request.path_params["model"] == "Товары" else "category"
                        request.session["error_message"] = "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                        return RedirectResponse(url=f"/admin/{model_view}/list", status_code=status.HTTP_303_SEE_OTHER)
                    else:
                        if cnt_row == cnt_to_add-1:
                            return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
                        else:
                            model_view = "product" if request.path_params["model"] == "Товары" else "category"
                            request.session["warning_message"] = f"Удалось добавить {cnt_to_add} из {cnt_row-1} записей"
                            return RedirectResponse(url=f"/admin/{model_view}/list", status_code=status.HTTP_303_SEE_OTHER)
                        
        model_view = "product" if request.path_params["model"] == "Товары" else "category"
        request.session["error_message"] = "ОШИБКА ОБРАБОТКИ ФАЙЛА: Выбран не верный формат файла"
        return RedirectResponse(url=f"/admin/{model_view}/list", status_code=status.HTTP_303_SEE_OTHER)