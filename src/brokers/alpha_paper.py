from .database import sqlite_db
from .base import BrokerBase
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
paperbroker_logger = logging.getLogger(__name__)


subscribed_tokens = []


class PaperBroker(BrokerBase):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def initialize(self, **kwargs):
        pass

    def subscribe(self, identifier: str):
        if identifier in subscribed_tokens:
            paperbroker_logger.info(f'Subscribed to {identifier}')
            pass
        else:
            paperbroker_logger.info(f'Subscribing to {identifier}')
            # subscription logic here

    def unsubscribe(self, identifier: str):
        if identifier not in subscribed_tokens:
            paperbroker_logger.info(f'Subscribing to {identifier}')
            # unsubscription logic here
        else:
            paperbroker_logger.info(f'Unsubscribed to {identifier}')
            pass

    def on_tick_data(self, data: Any):
        pass

    async def searchInstrument(self, tradingSymbol: str, exchange: str, exchangeToken: str):
        pass

    async def findMarginRequired(self, order: Dict):

        pass

    def place_order(self, order: Dict):
        symbol = order['tradingSymbol']
        quantity = order['quantity']
        price = order['price']
        order_type = order['order_type']
        product_type = order['product_type']

        result = sqlite_db.create_order(
            self.user_id, symbol, quantity, price, order_type, product_type)
        return result
