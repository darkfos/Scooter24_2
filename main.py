#Local
from ScooterBackend.settings.api_settings import APISettings

#ROUTES
from ScooterBackend.api.routes.user_router import user_router as user_router
from ScooterBackend.api.routes.authentication_router import auth_router as auth_router
from ScooterBackend.api.routes.category_router import category_router as category_router
from ScooterBackend.api.routes.admin_router import admin_router as admin_router
from ScooterBackend.api.routes.review_router import review_router as review_router
from ScooterBackend.api.routes.product_router import product_router as product_router
from ScooterBackend.api.routes.order_router import order_router as order_router
from ScooterBackend.api.routes.favourite_router import favourite_router as favourite_router
from ScooterBackend.api.routes.history_buy_router import history_buy_router as history_buy_router
from ScooterBackend.api.routes.type_worker_router import type_worker_router as type_worker_router
from ScooterBackend.api.routes.vacancies_router import vacancies_router as vacancies_router
from ScooterBackend.api.routes.general_router import api_v1_router


#Other libraries
import uvicorn
import logging
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def connection_db(app: FastAPI) -> None:
    #lifespan for db
    #await db_work.create_tables()
    #yield
    pass


#Application (API)
app: FastAPI = FastAPI(
    title="Scooter API",
    description="Программный интерфейс для сайта по продаже авто деталей",
    #lifespan=connection_db
)


###CORS###
origins = [
    "*",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Include routers
routers = (
    admin_router,
    auth_router,
    user_router,
    category_router,
    product_router,
    review_router,
    order_router,
    history_buy_router,
    favourite_router,
    type_worker_router,
    vacancies_router
)

for router in routers:
    api_v1_router.register_router(new_router=router)

app.include_router(api_v1_router.get_api_v1)


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