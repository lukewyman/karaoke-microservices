from fastapi import FastAPI
from .api import router
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.include_router(router)