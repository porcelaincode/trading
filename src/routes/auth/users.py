from fastapi import APIRouter, Request
from utils import logger
from database import Sqlite

router = APIRouter()


@router.post("/login")
async def login(request: Request):
    logger.info('Login request: ', request)
    return


@router.post("/register")
async def login(request: Request):
    logger.info('Register request: ', request.body)
    clientId, brokerName, apiKey, apiSecret, *req = request.body
    sqlite_db = Sqlite()
    res = sqlite_db.create_user(
        brokerClientId=clientId, brokerName=brokerName, apiKey=apiKey, apiSecret=apiSecret)
    return res
