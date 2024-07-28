from utils import logger
from broker.broker_base import BrokerBase
from kiteconnect import KiteConnect, KiteTicker


class ZerodhaKite(BrokerBase):
    def __init__(self, authorized=False):
        self.client: KiteConnect = None
        self.access_token = None
        self.api_key = None
        self.authorized = authorized

    def initialize(self, api_key, api_secret, request_token):
        self.api_key = api_key
        self.api_secret = api_secret

        try:
            self.client = KiteConnect(api_key=self.api_key)
            data = self.client.generate_session(
                request_token, api_secret=self.api_secret)
            self.access_token = data["access_token"]
            self.client.set_access_token(self.access_token)
            logger.info(
                f"Zerodha client initialized with API key: {self.api_key}")
            return self.client
        except Exception as e:
            logger.error(f"Failed to initialize Zerodha client: {e}")
            return None

    def authorize(self):
        if self.access_token:
            self.authorized = True
            logger.info("Zerodha client successfully authenticated")
            return True
        else:
            logger.error("Zerodha client authorization failed")
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
