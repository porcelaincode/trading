
import sys  # noqa
import os  # noqa
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'src')))  # noqa

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from .config import env
from contextlib import asynccontextmanager
import logging

from .routes.auth import users
from .routes.brokers import icici

from .socket.broker import connect_marketdata, clean_sockets
from .socket.server import consume_broadcast_signals, manager

logging.basicConfig(level=logging.INFO)
fastapi_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_marketdata()
    consume_broadcast_signals()
    yield
    clean_sockets()

app = FastAPI(lifespan=lifespan, debug=True)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    fastapi_logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    fastapi_logger.info(f"Response status: {response.status_code}")
    return response


app.include_router(users.router, prefix="/api/v1/auth/users")

app.include_router(icici.router, prefix="/api/v1/brokers/icici")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    fastapi_logger.info(f'Running application on {env.HOST}:{env.PORT}')
    uvicorn.run(app, host=env.HOST, port=env.PORT)
