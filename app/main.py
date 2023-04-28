from fastapi import FastAPI

from app.api.handlers.image import router as image_router
from app.api.middlewares.error import ErrorMiddleware


app = FastAPI()
app.add_middleware(ErrorMiddleware)
app.include_router(image_router)
