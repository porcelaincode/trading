import asyncio
from utils import logger

from broker.broker_base import BrokerBase


class TradingEngine:
    def __init__(self, client: BrokerBase, instrument_prefix, profit_target=0, loss_limit=0):
        self.client = client
        self.instrument_prefix = instrument_prefix
        self.profit_target = profit_target
        self.loss_limit = loss_limit
        self.positions = {}
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info(
            f"Starting Trading Engine for {self.instrument_prefix}")
        self.client.subscribe(
            self.instrument_prefix)

    async def stop(self):
        self.is_running = False
        logger.info(
            f"Stopping Trading Engine for {self.instrument_prefix}")
        self.client.unsubscribe(self.instrument_prefix)
