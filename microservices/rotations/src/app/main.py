from fastapi import FastAPI
from .api import router
from .logger import logger
from .middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
logger.info('Starting rotations API...')

app.include_router(router)