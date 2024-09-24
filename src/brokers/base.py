from abc import ABC, abstractmethod

class BrokerBase(ABC):
    def __init__(self):
        pass

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