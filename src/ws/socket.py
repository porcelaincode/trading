# module imports
import asyncio
import json
import datetime
import websockets
from logging import Logger

# project imports
from database import sqlite
from ws.socket_base import WebSocketBase
from config import env

class WebSocket(WebSocketBase):
    def __init__(self, logger: Logger):
        self.clients = set()
        self.db = sqlite()
        self.logger = logger

    async def handler(self, websocket, path):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)

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
            "datetime": datetime.datetime.now().isoformat()
        }
        await self.broadcast("signal", data)

    def run(self):
        server = websockets.serve(self.handler, env.WEBSOCKET_HOST, env.WEBSOCKET_PORT)
        self.logger.info('Websocket initialised')
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()