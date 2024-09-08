from sqladmin import Admin, ModelView
from typing import Type, List
from database.db_worker import db_work
from fastapi import FastAPI


class AdminPanel:

    def __init__(self, app: FastAPI) -> None:
        self.admin_panel: Type[Admin] = Admin(engine=db_work.db_engine, app=app)

    def initialize_models_view(self, models: List[ModelView]) -> None:
        for model in models:
            self.admin_panel.add_view(model)