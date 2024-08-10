from abc import ABC, abstractmethod
import pickle
from utils import logger
from pydantic import Any
from database import Sqlite


class BrokerBase(ABC):
    def __init__(self, clientId: str, broker: str) -> Any | None:
        self.db = Sqlite()
        self.clientId = clientId
        self.broker = broker

        # TODO: save client instance in memory somewhere and restore when server reboot is complete
        # broker_instance = self.db.get_client_instance(
        #     clientId=clientId, broker=broker)
        # if broker_instance:
        #     return pickle.loads(broker_instance)
        # else:
        #     logger.info(
        #         'No prior instance found for this client and broker, creating fresh broker instance. Please initialize and authorize.')
        #     return None

    @abstractmethod
    def initialize(self, **kwargs):
        pass

    @abstractmethod
    def authorize(self, consumer_key, otp):
        '''
        Most brokers implement 2fa so this method should be used to initialize session using client sdks or http requests.
        '''
        pass

    @abstractmethod
    def subscribe(self):
        '''
        Calling broker sdks/http request to subscribe for market data of instruments. 
        It also inserts data into 'active_instruments' database in order to keep a track of active and subscribed instruments.
        This function should also be called when initial server start up takes place and a clients open orders and positions are loaded into redis as hot cache.
        '''
        pass

    @abstractmethod
    def unsubscribe(self):
        '''
        Sends unsubscribe request to broker sdk/http request in order to stop recieving marketdata ticks for a particular innocent. It also removes the subscribed instrument from database
        '''
        pass

    @abstractmethod
    async def on_tick_data(self):
        pass

    @abstractmethod
    async def searchInstrument(self):
        pass

    @abstractmethod
    async def findMarginRequired(self):
        pass

    @abstractmethod
    def place_order(self):
        pass

    @abstractmethod
    def cleanup(self):
        '''
        1. emits signal on socket that client is closing.\n
        2. stops trading engine manager accessing this broker client.\n
        3. stops all trading engines accessing this broker client.\n
        4. fetch all active subscribed instruments of client and broker from `active_instruments` and send unsubscription request to broker
        5. disconnects broker client from system.\n
        6. emits signal to cancel all pending orders (optional).\n
        7. emits signal to close all positions (optional)
        '''
        pass

    def backup(self, instance):
        '''
        Stores serialized client instance in db for backup
        '''
        # TODO: implement backing up of client instance, client.backup(client) may be one way this method is called. nasty
        # self.db.store_client_instance(
        #     clientId=self.clientId, broker=self.broker, instance=pickle.dumps(instance))
        pass
