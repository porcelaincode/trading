import json

from broker.broker_base import BrokerBase
from breeze_connect import BreezeConnect

from utils import logger

from constants import PositionEvents, OrderEvents, OrderStatus

from utils import publish_message


class IciciBreeze(BrokerBase):
    def __init__(self, clientId: str, authorized=False):
        # tries to load instance from memory if there exists any, else
        # res = super().__init__(clientId=clientId, broker='icici_breeze')
        # if res:
        #     self = res
        # else:
        #     self.clientId = clientId
        #     self.authorized = authorized
        #     self.client: BreezeConnect = None
        # pass
        self.clientId = clientId
        self.authorized = authorized
        self.client: BreezeConnect = None

    def initialize(self, api_key: str):
        self.breeze = BreezeConnect(api_key=api_key)
        logger.info('Initialized breeze session for client: ', self.clientId)
        return {'message': f'Initialized breeze client for {self.clientId}. Please go to https://api.icicidirect.com/apiuser/login?api_key={api_key} to initialize login'}

    def authorize(self, secret_key, session_token):
        message = ''
        try:
            self.breeze.generate_session(api_secret=secret_key,
                                         session_token=session_token)
            message = f'Initialized breeze session for client: {self.clientId}'
            logger.info(message, self.clientId)
            self.breeze.on_ticks = self.on_tick_data
            self.breeze.ws_connect()
        except Exception as e:
            message = f'Error occured while generating session for {self.clientId}'
            logger.error(message + ' with error: ', e)

        return {'message': message}

    def cleanup(self):
        # close positions
        closePositionsMessage = json.dumps({
            "eventType": PositionEvents.CLOSE,
        })
        publish_message(queue='positions', message=closePositionsMessage)

        # cancel open orders
        cancelOrdersMessage = json.dumps({
            "eventType": OrderEvents.CANCEL,
            "data": {
                "orderType": OrderStatus.OPEN
            }
        })
        publish_message(queue='orders', message=cancelOrdersMessage)

        self.breeze.ws_disconnect()
        pass

    def on_tick_data(self, ticks):
        print('ticks: ', ticks)
        return

    def subscribe(self):
        return {}

    def unsubscribe(self):
        return {}
