from fastapi import FastAPI, Request, WebSocket
from config import env
from contextlib import asynccontextmanager

from utils import logger
from routes.auth import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan, debug=True)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


app.include_router(users.router, prefix="/api/v1/auth/users")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=env.HOST, port=env.PORT)