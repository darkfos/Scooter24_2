#Local
from settings import APISettings

#Other
from fastapi import FastAPI
import uvicorn
import logging


#Application (API)
app: FastAPI = FastAPI(
    title="Scooter API",
    description="Программный интерфейс для сайта по продаже авто деталей")


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