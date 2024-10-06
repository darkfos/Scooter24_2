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

    @override
    @login_required
    async def load_data(self, request: Request):

        # form data
        file: UploadFile  = (await request.form()).get("csv_file")
        data_model = request.path_params

        if file:
            if ".csv" in file.filename or ".xlsx" in file.filename:
                
                # Decode data file
                file_data = (await file.read()).decode("UTF-8")
                file_object = StringIO(file_data)
                file_data = pandas.read_csv(file_object, comment="#", sep=";")
                df = pandas.DataFrame(file_data)

                # Session
                session = EngineRepository()

                data_to_response: str = ""

                if request.path_params["model"] == "Товары":
                    data_to_response = "product"
                elif request.path_params["model"] == "Категории":
                    data_to_response = "category"
                else:
                    data_to_response = "sub-category"

                match data_model.get("model"):
                    case "Товары":
                        return await self.add_product(request=request, file=df, session=session, data_to_response=data_to_response)
                    case "Категории":
                        return await self.add_category(request=request, file=df, session=session, data_to_response=data_to_response)
                    case "Подкатегории":
                        return await self.add_sub_category(request=request, file=df, session=session, data_to_response=data_to_response)
                    case _:
                        request.session["error_message"] = "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось найти подходящую модель"
                        model_view = "product" if request.path_params["model"] == "Товары" else "category"
                        return RedirectResponse(url=f"/admin/{model_view}/list", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    
    @staticmethod
    async def add_product(request: Request, file: pandas.DataFrame,
                        session: EngineRepository, data_to_response: str) -> Response:
        """
        Добавление новых продуктов
        """

        cnt_to_add: int = 0
        cnt_row: int = 0


        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.iterrows():
                    category_data = id_subcat_1 = id_subcat_2 = None # Initial data for fk

                    # Find fk in other tables
                    if str(row["Категория"]) not in (None, "nan"):
                        category_data: Category = await session.category_repository.find_by_name(category_name=row["Категория"])
                    if str(row["Подкатегория первого уровня"]) not in (None, "nan"):
                        id_subcat_1: SubCategory = await session.subcategory_repository.find_by_name(name_subcategory=row["Подкатегория первого уровня"])
                    if str(row["Подкатегория второго уровня"]) not in (None, "nan"):
                        id_subcat_2: SubCategory = await session.subcategory_repository.find_by_name(name_subcategory=row["Подкатегория второго уровня"])

                    # replace type of object
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
                request.session["error_message"] = "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                return RedirectResponse(url=f"/admin/{data_to_response}/list", status_code=status.HTTP_303_SEE_OTHER)
            else:
                if cnt_row == cnt_to_add-1:
                    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
                else:
                    request.session["warning_message"] = f"Удалось добавить {cnt_to_add} из {cnt_row-1} записей"
                    return RedirectResponse(url=f"/admin/{data_to_response}/list", status_code=status.HTTP_303_SEE_OTHER)

    @staticmethod
    async def add_category(request: Request, file: pandas.DataFrame,
                           session: EngineRepository, data_to_response: str) -> Response:
        """
        Добавление новых категорий
        """

        cnt_to_add: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.itertuples():
                    name_category, image = row.split(",")
                    res_to_add = await session.category_repository.add_one(
                        Category(
                            name_category=name_category,
                            icon_category=image if image else None
                        )
                    )
                    if res_to_add: cnt_to_add += 1
                    cnt_row += 1
            except KeyError as ke:
                request.session["error_message"] = "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                return RedirectResponse(url=f"/admin/{data_to_response}/list", status_code=status.HTTP_303_SEE_OTHER)
            except ValueError as ve:
                request.session["error_message"] = "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не верный формат файла"
                return RedirectResponse(url=f"/admin/{data_to_response}/list", status_code=status.HTTP_303_SEE_OTHER)
            else:
                if cnt_row == cnt_to_add-1:
                    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
                else:
                    request.session["warning_message"] = f"Удалось добавить {cnt_to_add} из {cnt_row} записей"
                    return RedirectResponse(url=f"/admin/{data_to_response}/list", status_code=status.HTTP_303_SEE_OTHER)

    @staticmethod
    async def add_sub_category(request: Request, file: pandas.DataFrame,
                               session: EngineRepository, data_to_response: str) -> Response:
        """
        Добавление новых подкатегорий
        """

        cnt_to_add: int = 0
        cnt_row: int = 0


        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.iterrows():
                    res_to_add = await session.subcategory_repository.add_one(
                        SubCategory(
                            name=row.get("Подкатегория"),
                            level=row.get("Уровень"),
                            id_category=row.get("Категория"),
                            id_sub_category=row.get("П. подкатегории")
                        )
                    )
                if res_to_add: cnt_to_add += 1
                cnt_row += 1
            except KeyError as ke:
                request.session["error_message"] = "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                return RedirectResponse(url=f"/admin/{data_to_response}/list", status_code=status.HTTP_303_SEE_OTHER)
            else:
                if cnt_row == cnt_to_add-1:
                    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
                else:
                    request.session["warning_message"] = f"Удалось добавить {cnt_to_add} из {cnt_row-1} записей"
                    return RedirectResponse(url=f"/admin/{data_to_response}/list", status_code=status.HTTP_303_SEE_OTHER)