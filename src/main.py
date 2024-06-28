# module imports
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict
import logging
from contextlib import asynccontextmanager
from neo_api_client import NeoAPI

# project imports
from config import env
import utils.client
from ws import WebSocket
from trading import TradingEngineManager
from database import Sqlite
from broker import KotakNeo
from broker.broker_base import BrokerBase
from utils import client as client_utils


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to hold the broker client instances
broker_instances: Dict[str, BrokerBase] = {}
trading_engine_managers: Dict[str, TradingEngineManager] = {}
db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Sqlite()
    db.store_instruments()
    yield
    # maybe I should keep a backup of clients before server shutdown in case I need to reinitialise clients again
    db.shutdown_cleanup()
    db.close()


app = FastAPI(lifespan=lifespan)


class InitializeClientRequest(BaseModel):
    """
    Define the request model for the /intialize endpoint with broker name and their credentials. Currently only supporting broker kotak_neo
    """
    broker: str

    consumer_key: Optional[str]
    consumer_secret: Optional[str]
    environment: Optional[str]
    finkey: Optional[str]
    mobilenumber: Optional[str]
    password: Optional[str]


@app.post("/initialize")
async def authorize(req: InitializeClientRequest):
    message = ''
    client_key = client_utils.get_client_key(
        req.broker, mobile_number=req.mobilenumber)

    if client_key in broker_instances[req.broker].keys():
        message = f'Broker client for this registered mobile number {req.mobilenumber}, is already registered'
        logger.info(message)
        return message

    match req.broker:
        case 'kotak_neo':
            client = KotakNeo()
            res = client.initialize(consumer_key=req.consumer_key, consumer_secret=req.consumer_secret,
                                    environment=req.environment, fin_key=req.finkey, mobile_number=req.mobilenumber, password=req.password)
            if res:
                broker_instances[client_key] = res
                message = f'Successfully initialized broker client for kotak_neo. Authorize with otp sent to registered mobile number: {req.mobilenumber}'
                logger.info(message)
            else:
                message = f'Error initializing client with registered mobile number: {req.mobilenumber}'
                logger.error(message)
        case _:
            message = 'We are not supporting the requested broker at the moment'
            logger.error(message)

    return {'message': message}


class OTPRequest(BaseModel):
    """
    Define the request model for the /authorize endpoint
    """
    broker: str
    consumer_key: Optional[str]
    mobilenumber: str
    otp: str


@app.post("/authorize")
async def authorize(req: OTPRequest):
    global trading_engine_managers
    global broker_instances

    message = ''

    client_key = client_utils.get_client_key(
        req.broker, mobile_number=req.mobilenumber)
    broker_client = broker_instances[client_key]

    if broker_client is None:
        return {"message": "Client with this mobile number is not initialized yet"}

    match req.broker:
        case 'kotak_neo':
            broker_client.authorize(
                mobile_number=req.mobile_number, otp=req.otp)
        case _:
            message = 'We are not supporting the requested broker at the moment'
            logger.error(message)
            return {message: message}

    if client_key in trading_engine_managers.keys():
        return {"message": f'Manager for mobile number {req.mobilenumber} already exists.'}

    manager = TradingEngineManager(broker_client, db)
    trading_engine_managers[client_key] = manager
    await manager.start()

    return {"message": f'Trading manager initialized for client with registered mobile number {req.mobilenumber}.'}


class TradingEngineRequest(BaseModel):
    broker: str
    mobilenumber: str  # TODO: replace later with client id
    profit_target: float
    loss_limit: float


@app.post("/trading-engine")
async def manage_trading_engine(request: TradingEngineRequest):
    global trading_engine_managers

    client_key = client_utils.get_client_key(
        broker=request.broker, mobile_number=request.mobilenumber)

    if client_key in trading_engine_managers.keys():
        message = f"Trading engine manager not initialized for  mobile number: {request.mobilenumber}"
        logger.info(message)
        return {"message": message}

    trading_engine_manager = trading_engine_managers[client_key]

    try:
        # initialize trading engine manager for client with a set like profit and loss
        await trading_engine_manager.create_or_update_engine(request.profit_target, request.loss_limit)

        message = f"Initialized trading engine manager for successfully for mobile number: {request.mobilenumber} for {request.broker} trading engine manager"
        logger.info(message)
        return {"message": message}
    except Exception as e:
        message = f"Failed to manage trading engine: {e}"
        logger.error(message)
        return {"message": message}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.websocket('/ws')
async def websocket_endpoint():
    ws = WebSocket(logger=logger)
    ws.run()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=env.HOST, port=env.PORT)
