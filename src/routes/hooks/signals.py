from fastapi import APIRouter, Request
from utils import logger

router = APIRouter()


@router.post("/")
async def signalHook(request: Request):
    logger.info('signalHookRequest: ', request)
    return
