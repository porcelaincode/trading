import logging
import threading
import asyncio
from brokers.icici_direct import IciciBreeze

from config import env

logging.basicConfig(level=logging.INFO)
ws_logger = logging.getLogger("broker_ws")


class BrokerWebSocketManager:
    def __init__(self):
        self.client = IciciBreeze(clientId=env.MARKETDATA_CLIENT_ID)
        self.client.initialize(api_key=env.MARKETDATA_API_KEY)

    def connect(self):
        self.client.authorize(secret_key=env.MARKETDATA_SECRET_KEY,
                              session_token=env.MARKETDATA_SESSION_TOKEN, handle_ticks=self.handle_ticks)
        ws_logger.info('Marketdata streamer ready!')

    async def handle_ticks(self, ticks):
        """Listen for tick data from broker WebSocket and process it."""
        try:
            # Process tick data (e.g., store in memory or Redis)
            ws_logger.info(f"Received tick data: {ticks}")
        except Exception as e:
            ws_logger.error(f"Error receiving tick data: {e}")

    def disconnect(self):
        self.client.cleanup()


broker_ws_manager = BrokerWebSocketManager()

# Start the WebSocket connection and listen for data in background threads


def start_broker_websocket():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(broker_ws_manager.connect())
    loop.run_forever()


def connect_marketdata():
    ws_thread = threading.Thread(target=start_broker_websocket)
    ws_thread.start()


def clean_sockets():
    broker_ws_manager.disconnect()
