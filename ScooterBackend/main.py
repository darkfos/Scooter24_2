import logging.config
from src.scooter_backend_application import ScooterBackendApplication
from fastapi.responses import RedirectResponse
from fastapi import status, FastAPI
from typing import Type
import uvicorn
from logger import set_logger


set_logger()

scooter24: Type[ScooterBackendApplication] = ScooterBackendApplication()
app: Type[FastAPI] = scooter24.scooter24_app

# Redirect to docs
@app.get(path="/", status_code=status.HTTP_200_OK, response_class=RedirectResponse)
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(
        "/admin", status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )

if __name__ == "__main__":

    # Start project
    logging.info(msg="Start Project")
    uvicorn.run("main:app", reload=True)