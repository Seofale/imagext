from fastapi import FastAPI

from app.api.handlers import include_routers
from app.api.middlewares import include_middlewares

app = FastAPI()
include_routers(app)
include_middlewares(app)
