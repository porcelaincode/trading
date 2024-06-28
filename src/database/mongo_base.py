from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class MongoBase(ABC):
    @abstractmethod
    def create_collections(self):
        pass

    @abstractmethod
    def store_trade(self, trade_data):
        pass

    @abstractmethod
    def store_options_data(self, options_data):
        pass

    @abstractmethod
    def store_closed_position(self, position_data):
        pass

    @abstractmethod
    def store_orders(self, order_data):
        pass

    @abstractmethod
    def get_trade_pnl_between_dates(self, start_date, end_date):
        pass

    @abstractmethod
    def get_options_data_between_dates(self, start_date, end_date):
        pass

    @abstractmethod
    def get_closed_positions_between_dates(self, start_date, end_date):
        pass

    @abstractmethod
    def get_orders_between_dates(self, start_date, end_date):
        pass

    @abstractmethod
    def transfer_data_from_sqlite(self, sqlite_db_path):
        pass

    @abstractmethod
    def close(self):
        pass
