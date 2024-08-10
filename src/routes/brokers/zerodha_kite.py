from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from broker.zerodha_kite import ZerodhaKite
from utils import client as client_utils, logger
from trading import TradingEngineManager

router = APIRouter()

# in memory storage, have to figure how to save client instances
broker_instances = {}
trading_engine_managers = {}


class InitializeClientRequest(BaseModel):
    """
    Define the request model for the /initialize endpoint with broker name and their credentials.
    """
    broker: str
    api_key: Optional[str]
    api_secret: Optional[str]
    request_token: Optional[str]


@router.post("/initialize")
async def initialize(req: InitializeClientRequest):
    message = ''
    client_key = client_utils.get_client_key(req.broker, api_key=req.api_key)

    if client_key in broker_instances.keys():
        message = f'Broker client with API key {req.api_key} is already registered'
        logger.info(message)
        return {"message": message}

    client = ZerodhaKite()
    res = client.initialize(
        api_key=req.api_key, api_secret=req.api_secret, request_token=req.request_token)

    if res:
        broker_instances[client_key] = client
        message = f'Successfully initialized broker client for zerodha_kite. Authorize with the generated access token.'
        logger.info(message)
    else:
        message = f'Error initializing client with API key: {req.api_key}'
        logger.error(message)

    return {"message": message}


class AuthorizationRequest(BaseModel):
    """
    Define the request model for the /authorize endpoint
    """
    broker: str
    api_key: Optional[str]


@router.post("/authorize")
async def authorize(req: AuthorizationRequest):
    message = ''

    client_key = client_utils.get_client_key(req.broker, api_key=req.api_key)
    broker_client = broker_instances.get(client_key)

    if broker_client is None:
        return {"message": "Zerodha client with this API key is not initialized yet"}

    if req.broker == 'zerodha_kite':
        broker_client.authorize()
    else:
        message = 'We are not supporting the requested broker at the moment'
        logger.error(message)
        return {"message": message}

    if client_key in trading_engine_managers.keys():
        return {"message": f'Trading manager for API key {req.api_key} already exists.'}

    manager = TradingEngineManager(broker_client)
    trading_engine_managers[client_key] = manager
    await manager.start()

    return {"message": f'Trading manager initialized for client with API key {req.api_key}.'}
