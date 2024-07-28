from utils import logger
from broker.broker_base import BrokerBase
from neo_api_client import NeoAPI


class KotakNeo(BrokerBase):
    def __init__(self, authorized=False):
        self.client: NeoAPI = None
        self.authorized = authorized
        pass

    def initialize(self, consumer_key, consumer_secret, environment, fin_key, mobile_number, password):
        self.client = NeoAPI(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            environment=environment,
            neo_fin_key=fin_key
        )
        self.client.login(
            mobilenumber=mobile_number, password=password)

        logger.info(
            f"kotak_client initialized for mobile_number: {mobile_number} for consumer_key: {consumer_key}")

        return self.client

    def authorize(self, mobile_number, otp):
        try:
            res = self.client.session_2fa(OTP=otp)
            logger.info(
                f"kotak_client successfully authenticated for {mobile_number}")
            return res
        except Exception as e:
            logger.error(f"Failed to authenticate kotak_client: {e}")

    def subscribe(self, instrument):
        pass

    def unsubscribe(self, instrument):
        pass
