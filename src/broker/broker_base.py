from abc import ABC, abstractmethod


class BrokerBase(ABC):
    @abstractmethod
    def initialize(self, **kwargs):
        pass

    @abstractmethod
    def authorize(self, consumer_key, otp):
        pass

    @abstractmethod
    def subscribe(self):
        pass

    @abstractmethod
    def unsubscribe(self):
        pass

    @abstractmethod
    def place_order(self):
        pass
