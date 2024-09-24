from abc import ABC, abstractmethod


class SqliteBase(ABC):
    @abstractmethod
    def create_tables(self):
        pass
    
    @abstractmethod
    def create_tables(self):
        pass
    
    @abstractmethod
    def update_user_token(self):
        pass

    @abstractmethod
    def close(self):
        pass