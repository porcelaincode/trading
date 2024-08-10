# module imports
from fastapi import FastAPI, Request, WebSocket
from typing import Dict
from contextlib import asynccontextmanager

# project imports
from database import Sqlite
from app_config import env
from ws import WebSocketManager
from trading import TradingEngineManager, MarketDataManager
from utils import logger

# routes
from broker.broker_base import BrokerBase
from routes.brokers import icici_breeze, kotak_neo, fyers_api, zerodha_kite
from routes.auth import users
from routes.hooks import orders, positions, signals

# Global variable to hold the broker client instances
broker_instances: Dict[str, BrokerBase] = {}
trading_engine_managers: Dict[str, TradingEngineManager] = {}
websocket_manager = WebSocketManager()
# marketdata_manager = MarketDataManager()

db: Sqlite = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Sqlite()
    db.store_instruments()
    yield
    # maybe I should keep a backup of clients and active positions before server shutdown in case I need to reinitialise clients again
    db.shutdown_cleanup()
    db.close()


app = FastAPI(lifespan=lifespan, debug=True)

app.include_router(icici_breeze.router, prefix="/api/v1/brokers/icici")
app.include_router(kotak_neo.router, prefix="/api/v1/brokers/kotak")
app.include_router(fyers_api.router, prefix="/api/v1/brokers/fyers")
app.include_router(zerodha_kite.router, prefix="/api/v1/brokers/zerodha")

app.include_router(users.router, prefix="/api/v1/auth/users")

app.include_router(orders.router, prefix="/api/v1/hooks/orders")
app.include_router(positions.router, prefix="/api/v1/hooks/positions")
app.include_router(signals.router, prefix="/api/v1/hooks/signals")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.handler(websocket)


# @app.websocket("/ws/{broker_name}")
# async def websocket_endpoint(websocket: WebSocket, broker_name: str):
#     await websocket.accept()

#     marketdata_manager.switch_broker(broker_name)

#     # Resubscribe all instruments to the new broker
#     subscribed_instruments = marketdata_manager.get_subscribed_instruments()
#     for instrument in subscribed_instruments:
#         await marketdata_manager.active_broker.subscribe([instrument])

#     while True:
#         data = await websocket.receive_json()
#         if 'subscribe' in data:
#             marketdata_manager.subscribe_instrument(data['subscribe'])
#         elif 'unsubscribe' in data:
#             marketdata_manager.unsubscribe_instrument(data['unsubscribe'])

#         # Send market data to client
#         market_data = await marketdata_manager.get_market_data()
#         await websocket.send_json(market_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=env.HOST, port=env.PORT)
