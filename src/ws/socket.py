# module imports
import asyncio
import json
from fastapi import WebSocket

# project imports
from database import Sqlite
from ws.socket_base import WebSocketBase
from config import env
from utils.datetime import get_local_datetime
from utils.logger import fastapi_logger


class WebSocketManager(WebSocketBase):
    def __init__(self):
        self.clients = []
        self.db = Sqlite()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.clients.remove(websocket)

    async def handler(self, websocket: WebSocket):
        await self.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                data = json.loads(data)
                await self.handle_message(data)
        except Exception as e:
            fastapi_logger.error(
                'Disruption in websocket connection. Disconnecting client with exception', e)
            await self.disconnect(websocket)

    async def handle_message(self, data):
        # This is where incoming messages would be handled
        pass

    async def broadcast(self, event, data):
        if self.clients:
            message = json.dumps({"event": event, "data": data})
            await asyncio.wait([client.send(message) for client in self.clients])

    async def on_order_placed(self, order_data):
        await self.broadcast("order_placed", order_data)

    async def on_order_updated(self, order_data):
        await self.broadcast("order_updated", order_data)

    async def on_order_cancelled(self, order_data):
        await self.broadcast("order_cancelled", order_data)

    async def on_position_open(self, position_data):
        await self.broadcast("position_open", position_data)

    async def on_position_partially_closed(self, position_data):
        await self.broadcast("position_partially_closed", position_data)

    async def on_position_closed(self, position_data):
        await self.broadcast("position_closed", position_data)

    async def emit_signal(self, text):
        data = {
            "text": text,
            "datetime": get_local_datetime()
        }
        await self.broadcast("signal", data)

    # def run(self):
    #     server = websockets.serve(
    #         self.handler, env.WEBSOCKET_HOST, env.WEBSOCKET_PORT)
    #     self.fastapi_logger.info('Websocket initialised')
    #     asyncio.get_event_loop().run_until_complete(server)
    #     asyncio.get_event_loop().run_forever()
