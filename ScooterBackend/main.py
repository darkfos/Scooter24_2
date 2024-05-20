#Local
from settings import APISettings, DatabaseSettings
from database.db_worker import db_work
from database.mainbase import MainBase
##Tables##
from database.models.category import Category
from database.models.product import Product
from database.models.user import User
from database.models.favourite import Favourite
from database.models.review import Review
from database.models.history_buy import HistoryBuy
from database.models.order import Order


#Other
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import uvicorn
import logging


@asynccontextmanager
async def connection_db(app: FastAPI) -> None:
    #lifespan for db
    await db_work.create_tables(MainBase=MainBase)
    yield


#Application (API)
app: FastAPI = FastAPI(
    title="Scooter API",
    description="Программный интерфейс для сайта по продаже авто деталей",
    lifespan=connection_db
)


#Redirect to docs
@app.get(path="/", status_code=status.HTTP_200_OK, response_class=RedirectResponse)
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")


#Point of entry
if __name__ == "__main__":

    #Settings for run app
    sett: APISettings = APISettings()
    try:
        uvicorn.run(
            app="main:app",
            host=sett.api_host,
            port=sett.api_port,
            reload=sett.reload
        )
    except Exception as ex:
        logging.critical(msg="API cancel")