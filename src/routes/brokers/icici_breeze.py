from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse, RedirectResponse

from utils import fastapi_logger, datetime

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
        fastapi_logger.error(f"Failed to parse JSON payload: {e}")
        message = e
        try:
            form_data = await request.form()
            payload = dict(form_data)
        except Exception as e:
            fastapi_logger.error(f"Failed to parse form data: {e}")
            message = e
            payload = {}

    fastapi_logger.info(f'Payload recieved: {payload}')

    if (payload['API_Session']):
        url = "https://alphaedge.vatsalpandya.com?authorized=True"
        response = RedirectResponse(url)
        headers = {
            "broker": "ICICI",
            "datetime": str(datetime.get_local_datetime()),
            "token": "ABC123456",
        }
        for key, value in headers.items():
            response.headers[key] = value
        return response
    else:
        return JSONResponse(content={"authorized": False, "message": message})
