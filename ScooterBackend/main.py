#Local
from settings.api_settings import APISettings

#ROUTES
from api.routes.user_router import user_router as user_router
from api.routes.authentication_router import auth_router as auth_router
from api.routes.category_router import category_router as category_router
from api.routes.admin_router import admin_router as admin_router
from api.routes.review_router import review_router as review_router
from api.routes.product_router import product_router as product_router
from api.routes.order_router import order_router as order_router
from api.routes.favourite_router import favourite_router as favourite_router
from api.routes.history_buy_router import history_buy_router as history_buy_router
from api.routes.type_worker_router import type_worker_router as type_worker_router
from api.routes.vacancies_router import vacancies_router as vacancies_router
from api.routes.page_router import page_router
from api.routes.general_router import api_v1_router


#Other libraries
import uvicorn
import logging
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
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
    description="Программный интерфейс для сайта по продаже мото деталей",
    #lifespan=connection_db
)
app.mount(
    "/static", StaticFiles(directory="static"), name="static"
)
app.include_router(page_router)


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
    return RedirectResponse("/site/main")


#Point of entry
if __name__ == "__main__":

    #Settings for run app
    sett: APISettings = APISettings()
    try:
        uvicorn.run(
            app="main:app",
            #reload=sett.reload
        )
    except Exception as ex:
        logging.critical(msg="API cancel")