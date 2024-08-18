import json
import logging

from base import BrokerBase
from breeze_connect import BreezeConnect

from utils import get_local_datetime
from rabbitmq import rabbitmq_client

logging.basicConfig(level=logging.INFO)
icici_direct_logger = logging.getLogger(__name__)


class IciciBreeze(BrokerBase):
    def __init__(self, clientId: str, authorized=False):
        self.clientId = clientId
        self.authorized = authorized
        self.client: BreezeConnect = None

    def initialize(self, api_key: str):
        self.breeze = BreezeConnect(api_key=api_key)
        icici_direct_logger.info(
            'Initialized breeze session for client: ', self.clientId)
        return {'message': f'Initialized breeze client for {self.clientId}. Please go to https://api.icicidirect.com/apiuser/login?api_key={api_key} to initialize login'}

    def authorize(self, secret_key, session_token):
        message = ''
        try:
            self.breeze.generate_session(api_secret=secret_key,
                                         session_token=session_token)
            message = f'Initialized breeze session for client: {self.clientId}'
            icici_direct_logger.info(message, self.clientId)
            self.breeze.on_ticks = self.on_tick_data
            self.breeze.ws_connect()

            message = {
                "broker": 'icici',
                "clientId": self.clientId,
                "date": get_local_datetime()
            }
            rabbitmq_client.publish_message('auth', json.dumps(message))
        except Exception as e:
            message = f'Error occured while generating session for {self.clientId}'
            icici_direct_logger.error(message + ' with error: ', e)

        return {'message': message}

    def cleanup(self):
        self.breeze.ws_disconnect()
        pass

    def on_tick_data(self, ticks):
        print('ticks: ', ticks)
        return

    def subscribe(self):
        return {}

    def unsubscribe(self):
        return {}
