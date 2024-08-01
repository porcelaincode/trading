from fastapi import APIRouter, Request
from utils import logger

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    logger.info('Login request: ', request)
    return
