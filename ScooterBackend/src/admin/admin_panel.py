from sqladmin import Admin, ModelView
from typing import Type, List
from src.database.db_worker import db_work
from fastapi import FastAPI
from src.settings.engine_settings import Settings

# Models
from src.admin import all_models

# Admin Authentication
from src.admin.admin_auth import AdminPanelAuthentication
from src.api.authentication.authentication_service import Authentication


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

        # initialize
        self.initialize_models_view(models=all_models)

    def initialize_models_view(self, models: List[ModelView]) -> None:
        for model in models:
            self.admin_panel.add_view(model)
