import json
import asyncio
from typing import List
from fastapi import WebSocket
from rabbitmq.client import rabbitmq_client


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


def consume_broadcast_signals():
    def callback(ch, method, properties, body):
        message = json.loads(body.decode())

        if message.get("eventType") == "signal":
            asyncio.run(manager.broadcast(message.get("signal")))

        rabbitmq_client.channel.basic_consume(
            queue='broadcast_signals',
            on_message_callback=callback,
            auto_ack=True
        )

        rabbitmq_client.channel.start_consuming()
