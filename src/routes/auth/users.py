import logging
from fastapi import APIRouter, Request

from ...database import sqlite_db
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
auth_logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login")
async def login(request: Request):
    auth_logger.info('Login request: ', request)
    return


class RegisterPayload(BaseModel):
    broker_client_id: str
    broker_name: str
    api_key: str
    api_secret: str
    is_admin: bool = False


@router.post("/register")
async def register(payload: RegisterPayload):
    result = sqlite_db.create_user(broker_client_id=payload.broker_client_id, broker_name=payload.broker_name,
                                   api_key=payload.api_key, api_secret=payload.api_secret, is_admin=payload.is_admin)
    return result


@router.get("/{broker}/{clientId}")
async def getUser(clientId: str, broker: str):
    result = sqlite_db.get_user(broker_client_id=clientId, broker_name=broker)
    return result


@router.get("/")
async def getAllUsers(request: Request):
    results = sqlite_db.get_all_users()
    return results


class DeletePayload(BaseModel):
    broker_client_id: str
    broker_name: str


@router.delete("/")
async def deleteUser(payload: DeletePayload):
    results = sqlite_db.delete_user(
        broker_client_id=payload.broker_client_id, broker_name=payload.broker_name)
    return results


class Updateaccess_tokenPayload(BaseModel):
    broker_client_id: str
    broker_name: str
    access_token: str


@router.patch("/")
async def updateUserToken(payload: Updateaccess_tokenPayload):
    results = sqlite_db.update_user_token(
        broker_client_id=payload.broker_client_id, broker_name=payload.broker_name, access_token=payload.access_token)
    return results
