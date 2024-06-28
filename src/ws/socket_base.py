from abc import ABC, abstractmethod

class WebSocketBase(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def on_order_placed(self, order_data):
        pass

    @abstractmethod
    def on_order_updated(self, order_data):
        pass

    @abstractmethod
    def on_order_cancelled(self, order_data):
        pass

    @abstractmethod
    def on_position_open(self, position_data):
        pass

    @abstractmethod
    def on_position_partially_closed(self, position_data):
        pass

    @abstractmethod
    def on_position_closed(self, position_data):
        pass

    @abstractmethod
    def emit_signal(self, data):
        pass