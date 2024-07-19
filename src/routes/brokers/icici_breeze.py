from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from utils import fastapi_logger

router = APIRouter()


class InitiateBreezeLoginPayload(BaseModel):
    api_key: str


@router.get('/intialize')
async def initiate_login(request: InitiateBreezeLoginPayload):
    """
    Request model for the /intialize endpoint
    """
    return {"redirect_link": f'https://api.icicidirect.com/apiuser/login?api_key={request.api_key}'}


@router.post("/login")
async def login_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        fastapi_logger.error(f"Failed to parse JSON payload: {e}")
        try:
            form_data = await request.form()
            payload = dict(form_data)
        except Exception as e:
            fastapi_logger.error(f"Failed to parse form data: {e}")
            payload = {}

    fastapi_logger.info(f"Received login payload: {payload}")
    return JSONResponse(content={"authorized": True})
