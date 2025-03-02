from sqladmin import Admin, ModelView
from starlette.routing import Route, Mount
from starlette.responses import RedirectResponse, Response
from starlette.applications import Starlette
from fastapi import status, UploadFile
from starlette.staticfiles import StaticFiles
from sqladmin.authentication import login_required
from typing import Type, List, override

from src.database.db_worker import db_work
from fastapi import FastAPI, Request

from src.settings.engine_settings import Settings
from io import StringIO

# Models
from src.admin import all_models

# Admin Authentication
from src.admin.admin_auth import AdminPanelAuthentication
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import EngineRepository
from src.admin.admin_panel_data_service import AdminPanelService
import pandas


class AdminPanel(AdminPanelService):
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

        # Admin starlette data
        self.starlette_data: Starlette = self.admin_panel.__dict__["admin"]

        # Add router
        self.starlette_data.routes.extend(
            [
                Route(
                    path="/load_data/{model}",
                    endpoint=self.load_data,
                    name="load_data",
                    methods=["POST", "GET"],
                ),
                Route(
                    path="/load_data/{model}/{update}",
                    endpoint=self.update_data,
                    name="update_data",
                    methods=["POST", "GET"],
                ),
            ]
        )

        self.starlette_data.routes.append(
            Mount(
                path="/static_sc24",
                app=self.statics_scooter24,
                name="static_sc24",
            )
        )

        # initialize
        self.initialize_models_view(models=all_models)

    def initialize_models_view(self, models: List[ModelView]) -> None:
        for model in models:
            self.admin_panel.add_view(model)

    @override
    @login_required
    async def index(self, request: Request) -> Response:
        """
        Index route which can be overridden to create dashboards.
        """
        request.session["error_message"] = ""
        request.session["warning_message"] = ""
        return await self.templates.TemplateResponse(
            request, "sqladmin/index.html"
        )

    @override
    @login_required
    async def load_data(self, request: Request):

        # form data
        file: UploadFile = (await request.form()).get("csv_file")
        data_model = request.path_params

        if file:
            if ".csv" in file.filename or ".xlsx" in file.filename:

                # Decode data file
                file_data = (await file.read()).decode("UTF-8")
                file_object = StringIO(file_data)
                file_data = pandas.read_csv(file_object, comment="#", sep=",")
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

                # fmt: off
                match data_model.get("model"):
                    case "Товары":
                        return await self.add_product(
                            request=request,
                            file=df,
                            session=session,
                            data_to_response=data_to_response,
                        )
                    case "Категории":
                        return await self.add_category(
                            request=request,
                            file=df,
                            session=session,
                            data_to_response=data_to_response,
                        )
                    case "Подкатегории":
                        return await self.add_sub_category(
                            request=request,
                            file=df,
                            session=session,
                            data_to_response=data_to_response,
                        )
                    case _:
                        request.session["error_message"] = (
                            "ОШИБКА ОБРАБОТКИ ФАЙЛА: "
                            "Не удалось найти подходящую модель"
                        )
                        model_view = (
                            "product"
                            if request.path_params["model"] == "Товары"
                            else "category"
                        )
                        return RedirectResponse(
                            url=f"/admin/{model_view}/list",
                            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                        )
                # fmt: onn

    @override
    @login_required
    async def update_data(self, request: Request):
        """
        Обновление данных в таблице
        """

        params_from_req = request.path_params
        file: UploadFile = (await request.form()).get("csv_file")
        model_view = (
            "product" if params_from_req["model"] == "Товары" else "category"
        )

        # Работа с файлом
        file_data = (await file.read()).decode("UTF-8")
        file_object = StringIO(file_data)
        file_data = pandas.read_csv(file_object, comment="#", sep=";")
        df = pandas.DataFrame(file_data)

        match params_from_req["model"]:
            case "Товары":
                await self.update_product(
                    request=request, engine=EngineRepository(), file=df
                )
            case "Категория":
                await self.update_category(
                    request=request,
                    file=df,
                    session=EngineRepository(),
                    data_to_response="category",
                )
            case _:
                return RedirectResponse(
                    url="/admin", status_code=status.HTTP_303_SEE_OTHER
                )

        return RedirectResponse(
            url=f"/admin/{model_view}/list",
            status_code=status.HTTP_303_SEE_OTHER,
        )
