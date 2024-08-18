from fastapi import FastAPI, Request, WebSocket
from config import env
from contextlib import asynccontextmanager
import logging

from routes.auth import users
from routes.brokers import icici

logging.basicConfig(level=logging.INFO)
fastapi_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan, debug=True)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    fastapi_logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    fastapi_logger.info(f"Response status: {response.status_code}")
    return response


app.include_router(users.router, prefix="/api/v1/auth/users")

app.include_router(icici.router, prefix="/api/v1/brokers/icici")

if __name__ == "__main__":
    import uvicorn
    fastapi_logger.info(f'Running application on {env.HOST}:{env.PORT}')
    uvicorn.run(app, host=env.HOST, port=env.PORT)
