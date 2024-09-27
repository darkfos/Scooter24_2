from sqladmin import Admin, ModelView, expose
from starlette.routing import Route, Mount
from starlette.responses import RedirectResponse
from starlette.applications import Starlette
from fastapi import status, UploadFile
from starlette.staticfiles import StaticFiles
from sqladmin.authentication import login_required
from typing import Type, List
from src.database.db_worker import db_work
from fastapi import FastAPI, Request
from src.settings.engine_settings import Settings
from io import BytesIO, StringIO

# Models
from src.admin import all_models

# Admin Authentication
from src.admin.admin_auth import AdminPanelAuthentication
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import EngineRepository
from sqladmin import BaseView, expose
from fastapi import Request
from src.api.core.product_catalog.schemas.product_dto import ProductBase
from src.database.models.product import Product
from src.database.models.category import Category
from src.database.models.subcategory import SubCategory
import pandas, csv


class AdminPanel:
    def __init__(self, app: FastAPI) -> None:
        self.admin_panel_auth: Type[AdminPanelAuthentication] = (
            AdminPanelAuthentication(
                secret_key=Settings.auth_settings.jwt_secret_key,
                auth_service=Authentication(),
            )
        )

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

        # initialize
        self.initialize_models_view(models=all_models)

    def initialize_models_view(self, models: List[ModelView]) -> None:
        for model in models:
            self.admin_panel.add_view(model)

    @login_required
    async def load_data(self, request: Request):

        # form data
        file: UploadFile  = (await request.form()).get("csv_file")

        if file:
            file_data = (await file.read()).decode("UTF-8")

            file_object = StringIO(file_data)
            file_data = pandas.read_csv(file_object, comment="#", sep=";")
            df = pandas.DataFrame(file_data)
            session = EngineRepository()


            async with session:
                session: EngineRepository = session

                for index, row in df.iterrows():

                    category_data = id_subcat_1 = id_subcat_2 = None
                    print(row["Категория"], row["Подкатегория второго уровня"], row["Подкатегория первого уровня"])

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


        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)