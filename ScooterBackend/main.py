from src.scooter_backend_application import ScooterBackendApplication
from fastapi.responses import RedirectResponse
from fastapi import status, FastAPI
from typing import Type
import uvicorn
import logging


if __name__ == "__main__":

    # Logging
    logging.basicConfig(level=logging.INFO, filename="scooter24-log.log", filemode="w")

    scooter24: Type[ScooterBackendApplication] = ScooterBackendApplication()
    app: Type[FastAPI] = scooter24.scooter24_app

    # Redirect to docs
    @app.get(path="/", status_code=status.HTTP_200_OK, response_class=RedirectResponse)
    async def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse(
            "/admin", status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

    # Start project
    logging.info(msg="Start Project")

    uvicorn.run(app=app)
