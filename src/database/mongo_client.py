from time import sleep
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from ..config import env

logging.basicConfig(level=logging.INFO)
mongo_logger = logging.getLogger(__name__)

mongo_connection_string = env.MONGO_CONNECTION_STRING
mongo_db_name = env.MONGO_DB_NAME


class MongoDBClient:
    def __init__(self, db_name, max_retries=20):
        self.db_name = db_name
        self.max_retries = max_retries
        self.client = MongoClient(mongo_connection_string)
        self._connect()

    def _connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.client.admin.command('ping')
                mongo_logger.info("Connected to MongoDB!!!")
                return
            except ConnectionFailure:
                retries += 1
                mongo_logger.info(f"Attempt {retries} to reconnect...")
                sleep(retries * 0.5)
        raise Exception("Too many retries.")

    def get_database(self):
        return self.client[self.db_name]


mongo_client = MongoDBClient(db_name=mongo_db_name)
db = mongo_client.get_database()


class Store:
    def __init__(self, db):
        self.db = db


store = Store(db=db)
