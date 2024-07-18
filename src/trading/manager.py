from utils import fastapi_logger
from trading import TradingEngine
from database.sqlite_base import SqliteBase
from broker.broker_base import BrokerBase


class TradingEngineManager:
    def __init__(self, client: BrokerBase, db: SqliteBase):
        self.client = client
        self.database = db
        self.engines = {}
        self.is_running = False

    async def start(self):
        self.is_running = True
        fastapi_logger.info("Starting Trading Engine Manager")
        self.client.on_message = self.on_message
        self.client.on_error = self.on_error

    async def stop(self):
        self.is_running = False
        fastapi_logger.info("Stopping Trading Engine Manager")
        for engine in self.engines.values():
            await engine.stop()

    async def create_or_update_engine(self, profit_target, loss_limit):
        pass
