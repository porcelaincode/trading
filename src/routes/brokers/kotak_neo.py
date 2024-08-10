from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from broker import KotakNeo
from utils import client as client_utils, logger
from trading import TradingEngineManager

router = APIRouter()


class InitializeClientRequest(BaseModel):
    """
    Define the request model for the /intialize endpoint with broker name and their credentials.
    """
    broker: str
    consumer_key: Optional[str]
    consumer_secret: Optional[str]
    environment: Optional[str]
    finkey: Optional[str]
    mobilenumber: Optional[str]
    password: Optional[str]


@router.post("/initialize")
async def authorize(req: InitializeClientRequest):
    message = ''
    client_key = client_utils.get_client_key(
        req.broker, mobile_number=req.mobilenumber)

    if client_key in broker_instances[req.broker].keys():
        message = f'Broker client for this registered mobile number {req.mobilenumber}, is already registered'
        logger.info(message)
        return message

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

    return {'message': message}


class OTPRequest(BaseModel):
    """
    Define the request model for the /authorize endpoint
    """
    broker: str
    consumer_key: Optional[str]
    mobilenumber: str
    otp: str


@router.post("/authorize")
async def authorize(req: OTPRequest):
    global trading_engine_managers
    global broker_instances

    message = ''

    client_key = client_utils.get_client_key(
        req.broker, mobile_number=req.mobilenumber)
    broker_client = broker_instances[client_key]

    if broker_client is None:
        return {"message": "Kotak client with this mobile number is not initialized yet"}

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

    manager = TradingEngineManager(broker_client)
    trading_engine_managers[client_key] = manager
    await manager.start()

    return {"message": f'Trading manager initialized for client with registered mobile number {req.mobilenumber}.'}
