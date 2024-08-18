import logging
import json

from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse, RedirectResponse

from rabbitmq import rabbitmq_client
from database import sqlite_db

logging.basicConfig(level=logging.INFO)
icici_router = logging.getLogger(__name__)

router = APIRouter()


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
        icici_router.error(f"Failed to parse JSON payload: {e}")
        message = e
        try:
            form_data = await request.form()
            payload = dict(form_data)
        except Exception as e:
            icici_router.error(f"Failed to parse form data: {e}")
            message = e
            payload = {}

    if (payload['API_Session']):
        sqlite_db.update_user_token(broker_client_id=payload['user_id'],
                                    broker_name='icici', access_token=payload['API_Session'])
        redirect_url = "https://alphaedge.vatsalpandya.com"
        response = RedirectResponse(url=redirect_url)

        message = {
            "event": "LOGIN",
            "data": {
                "broker_client_id": payload['user_id'],
                "broker_name": 'icici',
            }
        }
        rabbitmq_client.publish_message('auth', json.dumps(message))
        return response
    else:
        return JSONResponse(content={"authorized": False, "message": message})
