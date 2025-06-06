import logging.config
from src.scooter_backend_application import ScooterBackendApplication
from fastapi.responses import RedirectResponse
from fastapi import status, FastAPI
from typing import Type
import uvicorn
from logger import set_logger
from faststream.rabbit import RabbitQueue
from src.settings.engine_settings import Settings

set_logger()

scooter24: Type[ScooterBackendApplication] = ScooterBackendApplication()
app: Type[FastAPI] = scooter24.scooter24_app


@app.get(
    path="/", status_code=status.HTTP_200_OK, response_class=RedirectResponse
)
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(
        "/admin", status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@app.on_event("startup")
async def startup_event() -> None:
    from src.other.broker.rabbit import broker

    await broker.connect()
    await broker.declare_queue(queue=RabbitQueue(name="email"))
    await broker.declare_queue(queue=RabbitQueue(name="transaction_send"))


if __name__ == "__main__":
    logging.info(msg="Start Project")
    uvicorn.run(
        app=app,
        host=Settings.api_settings.api_host,
        port=int(Settings.api_settings.api_port),
    )
