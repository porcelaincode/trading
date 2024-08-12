from utils import logger
from broker.broker_base import BrokerBase


class PaperBroker(BrokerBase):
    def __init__(self, authorized=False):
        self.client = None
        self.authorized = authorized

    def initialize(self, clientId: str):
        self.client = clientId
        return None

    def authorize(self):
        if self.clientId:
            self.authorized = True
            logger.info("Paper client successfully authenticated")
            return True
        else:
            logger.error("Paper client authorization failed")
            return False

    def subscribe(self, instrument):
        pass

    def unsubscribe(self, instrument):
        pass

    def place_order(self, tradingsymbol, quantity, order_type, transaction_type, product, price, stoploss, squareoff, trailing_stoploss):
        if not self.authorized:
            raise Exception("Client not authorized")

        try:
            order = self.client.place_order(
                variety=self.client.VARIETY_REGULAR,
                tradingsymbol=tradingsymbol,
                quantity=quantity,
                order_type=order_type,
                transaction_type=transaction_type,
                product=product,
                price=price,
                trigger_price=stoploss,
                squareoff=squareoff,
                stoploss=stoploss,
                trailing_stoploss=trailing_stoploss,
                validity=self.client.VALIDITY_DAY
            )
            logger.info(f"Order placed successfully: {order}")
            return order
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return None

    def cleanup(self, engine_ids: list[str]):
        return
