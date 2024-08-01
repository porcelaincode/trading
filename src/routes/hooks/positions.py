from fastapi import APIRouter, Request
from utils import logger

router = APIRouter()


@router.post("/")
async def positionHook(request: Request):
    logger.info('positionHookRequest: ', request)
    return
