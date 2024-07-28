from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from broker.fyers_api import FyersAPI
from utils import client as client_utils, logger
from trading import TradingEngineManager
from database import Sqlite

router = APIRouter()

# in memory storage, have to figure how to save client instances
broker_instances = {}
trading_engine_managers = {}


class InitializeClientRequest(BaseModel):
    """
    Define the request model for the /initialize endpoint with broker name and their credentials.
    """
    broker: str
    app_id: Optional[str]
    app_secret: Optional[str]
    redirect_uri: Optional[str]
    authorization_code: Optional[str]


@router.post("/initialize")
async def initialize(req: InitializeClientRequest):
    message = ''
    client_key = client_utils.get_client_key(req.broker, app_id=req.app_id)

    if client_key in broker_instances.keys():
        message = f'Broker client with app_id {req.app_id} is already registered'
        logger.info(message)
        return {"message": message}

    client = FyersAPI()
    client.initialize(app_id=req.app_id,
                      app_secret=req.app_secret, redirect_uri=req.redirect_uri)

    if client:
        broker_instances[client_key] = client
        message = f'Successfully initialized broker client for fyers_api. Authorize with authorization code sent to your email.'
        logger.info(message)
    else:
        message = f'Error initializing client with app_id: {req.app_id}'
        logger.error(message)

    return {"message": message}


class AuthorizationRequest(BaseModel):
    """
    Define the request model for the /authorize endpoint
    """
    broker: str
    app_id: Optional[str]
    authorization_code: str


@router.post("/authorize")
async def authorize(req: AuthorizationRequest):
    message = ''

    client_key = client_utils.get_client_key(req.broker, app_id=req.app_id)
    broker_client = broker_instances.get(client_key)

    if broker_client is None:
        return {"message": "Fyers client with this app_id is not initialized yet"}

    if req.broker == 'fyers_api':
        broker_client.authorize(req.authorization_code)
    else:
        message = 'We are not supporting the requested broker at the moment'
        logger.error(message)
        return {"message": message}

    if client_key in trading_engine_managers.keys():
        return {"message": f'Trading manager for app_id {req.app_id} already exists.'}

    db = Sqlite()
    manager = TradingEngineManager(broker_client, db)
    trading_engine_managers[client_key] = manager
    await manager.start()

    return {"message": f'Trading manager initialized for client with app_id {req.app_id}.'}
