import json

from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse, RedirectResponse

from app_config import env
from utils import logger, datetime, publish_message
from database import Sqlite
from constants import AppEvents, AppInstructions

router = APIRouter()
db = Sqlite()


class InitiateBreezeLoginPayload(BaseModel):
    api_key: str


@router.post('/initialize')
async def initiate_login(payload: InitiateBreezeLoginPayload):
    """
    Request model for the /initialize endpoint
    """
    return JSONResponse(f'https://api.icicidirect.com/apiuser/login?api_key={payload.api_key}')


@router.post("/login")
async def login_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON payload: {e}")
        message = e
        try:
            form_data = await request.form()
            payload = dict(form_data)
        except Exception as e:
            logger.error(f"Failed to parse form data: {e}")
            message = e
            payload = {}

    logger.info(f'Payload recieved: {payload}')

    if (payload['API_Session']):
        db.update_user_token(payload['user_id'],
                             'icici_breeze', payload['API_Session'])

        if payload['user_id'] == env.ICICI_API_USER_ID:
            publish_message('app', json.dumps({
                type: AppEvents.INSTRUCTION,
                message: AppInstructions.START
            }))
        else:
            redirect_url = "https://alphaedge.vatsalpandya.com?status=authorized"
            response = RedirectResponse(url=redirect_url)
            # headers = {
            #     "broker": "ICICI",
            #     "datetime": str(datetime.get_local_datetime()),
            #     "token": payload['API_Session'],
            # }
            # for key, value in headers.items():
            #     response.headers[key] = value
            return response
    else:
        return JSONResponse(content={"authorized": False, "message": message})
