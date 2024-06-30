import uvicorn
from fastapi import APIRouter, FastAPI

from src.auth.login_router import login_router
from src.auth.router import auth_router
from src.config import APP_PORT, DEBUG


def create_app():
    app = FastAPI(
        debug=DEBUG,
        docs_url="/api/docs/",
        title="Banking App"
    )

    return app

fastapi_app = create_app()

main_api_router = APIRouter()
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
fastapi_app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=APP_PORT)
