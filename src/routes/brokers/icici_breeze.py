from fastapi import APIRouter, Request
from utils import fastapi_logger

router = APIRouter()


@router.post("/login")
async def login_webhook(request: Request):
    payload = await request.json()
    fastapi_logger.info(f"Received login payload: {payload}")
    return {"authorized": True}
