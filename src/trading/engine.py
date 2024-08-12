import asyncio
from utils import logger
from broker.broker_base import BrokerBase


class TradingEngine:
    '''
    A trading engine exists as a entity of its own. It is actively searching for opportunities to make trades and is in direct contact with strategies and compute engine if needed. It is responsible for generating trading signals and placing trades. If this engine is turned off then all open orders of the 
    '''

    def __init__(self, client: BrokerBase, id: str):
        self.id = id
        self.client = client
        self.positions = {}
        self.is_running = False

    async def start(self):
        self.is_running = True
        # logger.info(
        #     f"Starting Trading Engine for {self.instrument_prefix}")
        # self.client.subscribe(
        #     self.instrument_prefix)

    async def stop(self):
        self.is_running = False
        # logger.info(
        #     f"Stopping Trading Engine for {self.instrument_prefix}")
        # self.client.unsubscribe(self.instrument_prefix)
