from fastapi import FastAPI

from .image import router as image_router


def include_routers(app: FastAPI) -> None:
    app.include_router(image_router)
