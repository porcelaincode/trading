from utils import logger
from broker.broker_base import BrokerBase
from fyers_apiv3 import fyersModel


class FyersAPI(BrokerBase):
    def __init__(self, authorized=False):
        self.client: fyersModel = None
        self.authorized = authorized
        self.session: fyersModel.SessionModel = None

    def initialize(self, app_id, app_secret, redirect_uri):
        self.session = fyersModel.SessionModel(
            client_id=self.app_id,
            secret_key=self.app_secret,
            redirect_uri=self.redirect_uri,
            response_type='code',
            grant_type='authorization_code'
        )
        generateTokenUrl = self.session.generate_authcode()

        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = generateTokenUrl

        logger.info(
            f"Fyers client initialized with app_id: {app_id} and redirect_uri: {redirect_uri}")

    def authorize(self, authorization_code):
        try:
            self.session = fyersModel.SessionModel(
                client_id=self.app_id, secret_key=self.app_secret, grant_type=authorization_code)
            self.session.set_token(authorization_code)
            response = self.session.generate_token()
            self.access_token = response['access_token']
            self.client = fyersModel.FyersModel(
                client_id=self.app_id, token=self.access_token)
            self.authorized = True
            logger.info("Fyers client successfully authenticated")
            return response
        except Exception as e:
            logger.error(f"Failed to authenticate Fyers client: {e}")

    def subscribe(self, instrument):
        pass

    def unsubscribe(self, instrument):
        pass

    def place_order(self, symbol, qty, order_type, side, productType, limitPrice, stopPrice):
        if not self.authorized:
            raise Exception("Client not authorized")

        order = {
            "symbol": symbol,
            "qty": qty,
            "type": order_type,
            "side": side,
            "productType": productType,
            "limitPrice": limitPrice,
            "stopPrice": stopPrice,
            "disclosedQty": 0,
            "validity": "DAY",
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0
        }

        try:
            response = self.client.place_order(order)
            logger.info(f"Order placed successfully: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
