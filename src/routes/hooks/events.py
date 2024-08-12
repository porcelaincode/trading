from fastapi import APIRouter, Request
from utils import logger

router = APIRouter()


@router.post("/")
async def eventHook(request: Request):
    logger.info('eventHookRequest: ', request)
    return
