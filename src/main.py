# module imports
from fastapi import FastAPI, Request, WebSocket
from typing import Dict
from contextlib import asynccontextmanager

# project imports
from database import Sqlite
from config import env
from ws import WebSocketManager
from trading import TradingEngineManager
from utils import fastapi_logger

# routes
from broker.broker_base import BrokerBase
from routes.brokers import icici_breeze, kotak_neo

# Global variable to hold the broker client instances
broker_instances: Dict[str, BrokerBase] = {}
trading_engine_managers: Dict[str, TradingEngineManager] = {}
websocket_manager = WebSocketManager()
db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Sqlite()
    db.store_instruments()
    yield
    # maybe I should keep a backup of clients before server shutdown in case I need to reinitialise clients again
    db.shutdown_cleanup()
    db.close()


app = FastAPI(lifespan=lifespan, debug=True)

app.include_router(icici_breeze.router, prefix="/api/v1/brokers/icici")
app.include_router(kotak_neo.router, prefix="/api/v1/brokers/kotak")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    fastapi_logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    fastapi_logger.info(f"Response status: {response.status_code}")
    return response


@app.websocket('/')
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.handler(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=env.HOST, port=env.PORT)
