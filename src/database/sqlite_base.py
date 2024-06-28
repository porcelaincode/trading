from abc import ABC, abstractmethod


class SqliteBase(ABC):
    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def store_instruments(self):
        pass

    @abstractmethod
    def store_order(self, order_id, order_params, status):
        pass

    @abstractmethod
    def today_stats(self):
        pass

    @abstractmethod
    def create_backup(self, mongo):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def close(self):
        pass
