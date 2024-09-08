from src.scooter_backend_application import ScooterBackendApplication
from fastapi.responses import RedirectResponse
from fastapi import status
import uvicorn


if __name__ == "__main__":

    scooter24 = ScooterBackendApplication()
    app = scooter24.scooter24_app

    #Redirect to docs
    @app.get(path="/", status_code=status.HTTP_200_OK, response_class=RedirectResponse)
    async def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse("/site/main")
    
    #Start project
    uvicorn.run(app=app)