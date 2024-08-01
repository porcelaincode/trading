from fastapi import APIRouter, Request
from utils import logger

router = APIRouter()


@router.post("/")
async def orderHook(request: Request):
    logger.info('orderHookRequest: ', request)
    return
